import datetime
from typing import Optional, List

from sqlalchemy import true
from sqlalchemy.orm import Session

from src.db import models, schemas


def query(db: Session, who: Optional[int] = None, which_boss: Optional[int] = None, conds: list = ()):
    cond1 = models.CurrentBattle.who == who if who else true()
    cond2 = models.CurrentBattle.which_boss == which_boss if which_boss else true()

    return db.query(models.CurrentBattle).where(cond1, cond2, *conds).order_by(models.CurrentBattle.when.desc())


def get(db: Session,
        who: Optional[int] = None,
        which_boss: Optional[int] = None,
        conds: list = ()) -> List[models.CurrentBattle]:
    return query(db, who, which_boss, conds).all()


def delete(db: Session, who: int = None, which_boss: int = None, conds: list = ()):
    cond1 = models.CurrentBattle.who == who if who else true()
    cond2 = models.CurrentBattle.which_boss == which_boss if which_boss else true()
    db.query(models.CurrentBattle).where(cond1, cond2, *conds).delete()
    db.commit()


def commit(db: Session, co: schemas.CurrentBattleCommit):
    # check if exists
    ret = get(db, co.who, co.which_boss)
    log = ret[0] if ret else models.CurrentBattle(**co.dict())

    if ret:
        # exists, update, do not modify `when`
        log.type = co.type
        log.comment = co.comment if co.comment else log.comment
    else:
        # not exists, insert new one, set `when`
        log.when = datetime.datetime.utcnow()
        db.add(log)

    # commit
    db.commit()
    return True, {'log': log}
