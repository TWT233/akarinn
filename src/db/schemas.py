from datetime import datetime, date
from typing import List

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
    detail: List[BossStatus]

    class Config:
        orm_mode = True


class BattleLogBase(BaseModel):
    who: str
    which_day: date
    which_round: int
    which_boss: int
    damage: int
    executor: str


class BattleLogCommit(BattleLogBase):
    pass


class BattleLog(BattleLogBase):
    when_commit: datetime
    is_defeat_boss: bool
    real_damage: int
    is_compensation: bool

    class Config:
        orm_mode = True


class Member(BaseModel):
    game_id: int
    permission: int
    contact_qq: str
    contact_khl: str

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
