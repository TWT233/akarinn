from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel


class BossStatus(BaseModel):
    number: int
    status: int
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


class Member(BaseModel):
    game_id: int
    permission: int
    contact_khl: str
    contact_qq: str

    class Config:
        orm_mode = True


class InfoClan(BaseModel):
    name: str
    desc: str
    khl_server: str
    qq_group: str

    class Config:
        orm_mode = True


class Info(BaseModel):
    clan: InfoClan
