from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date

from .init import Base


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    round = Column(Integer)


class BossStatus(Base):
    __tablename__ = 'boss_status'

    class StatusCode(Enum):
        UNDEF = 0
        DEFEATED = 1
        ACTIVE = 2
        WATING = 3

    boss_number = Column(Integer, primary_key=True)
    boss_status = Column(Integer)
    boss_hp = Column(Integer)
    boss_maxhp = Column(Integer)


class BattleLog(Base):
    __tablename__ = 'battle_log'

    id = Column(Integer, primary_key=True)

    who = Column(String)
    executor = Column(String)
    when_commit = Column(DateTime)
    which_day = Column(Date)
    which_round = Column(Integer)
    which_boss = Column(Integer)
    damage = Column(Integer)
    is_defeat_boss = Column(Boolean)
    is_compensation = Column(Boolean)
    real_damage = Column(Integer)


class CurrentBattle(Base):
    __tablename__ = 'current_battle'

    class StatusCode(Enum):
        UNDEF = 0
        ENTER = 1
        WAITING = 2

    id = Column(Integer, primary_key=True)

    who = Column(String)
    when = Column(DateTime)
    status = Column(Integer)
    comment = Column(String)


class Member(Base):
    __tablename__ = 'member'

    class Permission(Enum):
        MEMBER = 0
        VICE_LEADER = 1
        LEADER = 2

    game_id = Column(Integer, primary_key=True)
    permission = Column(Integer)
    contact_khl = Column(String)
    contact_qq = Column(String)