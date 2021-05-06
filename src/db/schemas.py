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

    class Config:
        orm_mode = True


class StatusRet(BaseModel):
    glob: Status
    detail: List[BossStatus]


class BattleLogBase(BaseModel):
    who: int
    which_day: date
    which_round: Optional[int]
    which_boss: Optional[int]
    damage: Optional[int]
    executor: int


class BattleLogCommit(BattleLogBase):
    sl: Optional[bool]
    pass


class BattleLog(BattleLogBase):
    when: datetime
    is_defeat_boss: Optional[bool]
    real_damage: Optional[int]
    type: models.BattleLog.Types

    class Config:
        orm_mode = True


class BattleLogRet(BaseModel):
    log: BattleLog
    status: StatusRet


class CurrentBattleBase(BaseModel):
    who: int
    executor: int
    which_boss: int
    type: models.CurrentBattle.Types
    comment: Optional[str]

    class Config:
        orm_mode = True


class CurrentBattleCommit(CurrentBattleBase):
    pass


class CurrentBattle(CurrentBattleBase):
    when: datetime


class CurrentBattleRet(BaseModel):
    log: CurrentBattle


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
