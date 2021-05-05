import datetime
from typing import Optional, List

from sqlalchemy import true
from sqlalchemy.orm import Session

from src.db import schemas, models
from . import status


def get(db: Session,
        who: Optional[int] = None,
        which_day: Optional[datetime.date] = None) -> List[models.BattleLog]:
    cond1 = models.BattleLog.who == who if who else true()
    cond2 = models.BattleLog.which_day == which_day if which_day else true()
    return db.query(models.BattleLog).where(cond1, cond2).order_by(models.BattleLog.when_commit.desc()).all()


def count(db: Session, who: Optional[int] = None, which_day: Optional[datetime.date] = None) -> float:
    logs = get(db, who=who, which_day=which_day)
    return float(sum(map(lambda i: 0.5 if (i.is_compensation or i.is_defeat_boss) else 1.0, logs)))


def is_compensation_now(db: Session, who: int, which_day: datetime.date) -> bool:
    return not count(db, who, which_day).is_integer()


def commit(db: Session, co: schemas.BattleLogCommit):
    current_status = status.get_status(db)
    current_boss_status = status.get_boss_status(db)

    # check round and boss
    if co.which_round != current_status.round:
        return False, 'wrong round'
    current_boss = current_boss_status[co.which_boss - 1]
    if current_boss.status != models.BossStatus.StatusCode.ACTIVE:
        return False, 'wrong boss'

    # check battle count
    if count(db, co.who, co.which_day) >= 3:
        return False, 'battle count limit exceeded'

    # battle log instantiation
    log = models.BattleLog()

    # check overkill
    if current_boss.hp <= co.damage:
        log.real_damage = current_boss.hp
        log.is_defeat_boss = True
    else:
        log.real_damage = co.damage
        log.is_defeat_boss = False

    # filling log
    log.who = co.who
    log.when_commit = datetime.datetime.utcnow()
    log.which_day = co.which_day
    log.which_round = co.which_round
    log.which_boss = co.which_boss
    log.damage = co.damage
    log.is_compensation = is_compensation_now(db, co.who, co.which_day)
    log.executor = co.executor

    # modify status
    current_boss.hp -= log.real_damage
    if log.is_defeat_boss:
        current_boss.status = models.BossStatus.StatusCode.DEFEATED
        db.commit()
        if not filter(lambda x: x.status != models.BossStatus.StatusCode.DEFEATED, current_boss_status):
            current_status.round += 1
            status.init_boss_status(db, current_status.round)

    # commit log
    db.add(log)
    db.commit()
    return True, log
