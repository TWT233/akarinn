import datetime
from typing import Optional, List

from sqlalchemy import true
from sqlalchemy.orm import Session

from src.db import schemas, models
from . import status, current_battle


def get(db: Session,
        who: Optional[int] = None,
        which_day: Optional[datetime.date] = None,
        conds: list = ()) -> List[models.BattleLog]:
    cond1 = models.BattleLog.who == who if who else true()
    cond2 = models.BattleLog.which_day == which_day if which_day else true()
    return db.query(models.BattleLog).where(cond1, cond2, *conds).order_by(models.BattleLog.when.desc()).all()


def count(db: Session, who: Optional[int] = None, which_day: Optional[datetime.date] = None) -> float:
    logs = get(db, who, which_day, [models.BattleLog.type != models.BattleLog.Types.SL])
    return float(sum(map(lambda x: 0.5 if x.type == models.BattleLog.Types.COMP or x.is_defeat_boss else 1.0, logs)))


def is_compensation_now(db: Session, who: int, which_day: datetime.date) -> bool:
    return not count(db, who, which_day).is_integer()


def is_sled(db: Session, who: int, which_day: datetime.date) -> bool:
    return len(get(db, who, which_day, [models.BattleLog.type == models.BattleLog.Types.SL])) > 0


def commit(db: Session, co: schemas.BattleLogCommit):
    current = status.get(db)

    # check sl
    if co.sl:
        if is_sled(db, co.who, co.which_day):
            return False, {'msg': 'sl has been used', 'status': current}
        log = models.BattleLog(who=co.who, when=datetime.datetime.utcnow(), which_day=co.which_day,
                               executor=co.executor, type=models.BattleLog.Types.SL)
        # commit log
        db.add(log)
        db.commit()
        # clean current battle
        current_battle.delete(db, log.who, log.which_boss)
        return True, {'log': log, 'status': current}

    # check round and boss
    if co.which_round != current['glob'].round:
        return False, {'msg': 'wrong round', 'status': current}
    current_boss = current['detail'][co.which_boss - 1]
    if current_boss.status != models.BossStatus.StatusCode.ACTIVE:
        return False, {'msg': 'wrong boss', 'status': current}

    # check battle count
    if count(db, co.who, co.which_day) >= 3:
        return False, {'msg': 'wrong boss', 'status': current}

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
    log.when = datetime.datetime.utcnow()
    log.which_day = co.which_day
    log.which_round = co.which_round
    log.which_boss = co.which_boss
    log.damage = co.damage
    log.type = models.BattleLog.Types.COMP if is_compensation_now(db, co.who,
                                                                  co.which_day) else models.BattleLog.Types.NORMAL
    log.executor = co.executor

    # modify status
    current_boss.hp -= log.real_damage
    if log.is_defeat_boss:
        current_boss.status = models.BossStatus.StatusCode.DEFEATED
        db.commit()
        # clean current battle
        current_battle.delete(db, which_boss=log.which_boss)
        if not filter(lambda x: x.status != models.BossStatus.StatusCode.DEFEATED, current['detail']):
            current['glob'].round += 1
            status.init_boss_status(db, current['glob'].round)

    # commit log
    db.add(log)
    db.commit()
    # clean current battle
    current_battle.delete(db, log.who, log.which_boss)
    return True, {'log': log, 'status': current}
