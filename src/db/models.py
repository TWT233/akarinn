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

    number = Column(Integer, primary_key=True)
    status = Column(Integer)
    hp = Column(Integer)
    max_hp = Column(Integer)


class BattleLog(Base):
    __tablename__ = 'battle_log'

    id = Column(Integer, primary_key=True)

    who = Column(Integer)
    executor = Column(Integer)
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

    who = Column(Integer)
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


class ClanInfo(Base):
    __tablename__ = 'clan_info'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    desc = Column(String)
    khl_server = Column(String)
    qq_group = Column(String)
