from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel

from src.db import models


class BossStatus(BaseModel):
    number: int
    status: models.BossStatus.StatusCode
    hp: int
    max_hp: int

    class Config:
        orm_mode = True


class Status(BaseModel):
    round: int


class StatusRet(BaseModel):
    round: int
    detail: List[BossStatus]

    class Config:
        orm_mode = True


class BattleLogBase(BaseModel):
    who: int
    which_day: date
    which_round: int
    which_boss: int
    damage: int
    executor: int


class BattleLogCommit(BattleLogBase):
    pass


class BattleLog(BattleLogBase):
    when_commit: datetime
    is_defeat_boss: bool
    real_damage: int
    is_compensation: bool

    class Config:
        orm_mode = True


class BattleLogRet(BaseModel):
    log: BattleLog
    status: StatusRet


class MemberBase(BaseModel):
    game_id: int
    contact_khl: Optional[str]
    contact_qq: Optional[str]


class Member(MemberBase):
    permission: models.Member.Permission

    class Config:
        orm_mode = True


class MemberAdd(MemberBase):
    permission: Optional[models.Member.Permission]
    op_key: Optional[str]


class InfoClan(BaseModel):
    name: str
    desc: str
    khl_server: str
    qq_group: str

    class Config:
        orm_mode = True


class Info(BaseModel):
    clan: InfoClan
