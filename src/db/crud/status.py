from typing import List

from sqlalchemy.orm import Session

from src.config import *
from src.db import models, schemas


def init_status(db: Session):
    # clear and insert
    db.query(models.Status).delete()
    db.add(models.Status(round=1))
    db.commit()


def init_boss_status(db: Session, round: int):
    # clear and insert
    db.query(models.BossStatus).delete()

    if conf_system_mode() == 'legacy':
        status_array = [models.BossStatus.StatusCode.ACTIVE] + [models.BossStatus.StatusCode.WAITING] * 4
    elif conf_system_mode() == 'new':
        status_array = [models.BossStatus.StatusCode.ACTIVE] * 5
    else:
        raise AssertionError('check system.yaml>system>mode: must be legacy or new')

    for i in range(5):
        boss = in_which_stage(round)['bosses'][i]
        db.add(models.BossStatus(number=i + 1, status=status_array[i], hp=boss['hp'], max_hp=boss['hp']))
    db.commit()


def get_status(db: Session) -> models.Status:
    dbr = db.query(models.Status).first()
    if not dbr:
        init_status(db)
        dbr = db.query(models.Status).first()
        # init boss status following status to reduce sql queries
        init_boss_status(db, dbr.round)
    return dbr


def get_boss_status(db: Session) -> List[models.BossStatus]:
    dbr = db.query(models.BossStatus).all()
    if len(dbr) != 5:
        init_boss_status(db, get_status(db).round)
        dbr = db.query(models.BossStatus).all()
    return dbr


def get(db: Session) -> schemas.StatusRet:
    return schemas.StatusRet(glob=get_status(db), detail=get_boss_status(db))
