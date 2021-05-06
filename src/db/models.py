import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Enum

from .init import Base


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    round = Column(Integer)


class BossStatus(Base):
    __tablename__ = 'boss_status'

    class StatusCode(enum.Enum):
        UNDEF = 'undef'
        DEFEATED = 'defeated'
        ACTIVE = 'active'
        WAITING = 'waiting'

    number = Column(Integer, primary_key=True)
    status = Column(Enum(StatusCode))
    hp = Column(Integer)
    max_hp = Column(Integer)


class BattleLog(Base):
    __tablename__ = 'battle_log'

    class Types(enum.Enum):
        UNDEF = 'undef'
        NORMAL = 'normal'
        SL = 'sl'
        COMP = 'compensation'

    id = Column(Integer, primary_key=True)

    who = Column(Integer)
    executor = Column(Integer)
    when = Column(DateTime)
    which_day = Column(Date)
    which_round = Column(Integer)
    which_boss = Column(Integer)
    damage = Column(Integer)
    is_defeat_boss = Column(Boolean)
    real_damage = Column(Integer)
    type = Column(Enum(Types))


class CurrentBattle(Base):
    __tablename__ = 'current_battle'

    class StatusCode(enum.Enum):
        UNDEF = 'undef'
        ENTER = 'enter'
        WAITING = 'waiting'

    id = Column(Integer, primary_key=True)

    who = Column(Integer)
    when = Column(DateTime)
    status = Column(Enum(StatusCode))
    comment = Column(String)


class Member(Base):
    __tablename__ = 'member'

    class Permission(enum.Enum):
        MEMBER = 'member'
        VICE_LEADER = 'vice_leader'
        LEADER = 'leader'
        EX_AID = 'ex_aid'

    game_id = Column(Integer, primary_key=True)
    permission = Column(Enum(Permission))
    contact_khl = Column(String)
    contact_qq = Column(String)


class ClanInfo(Base):
    __tablename__ = 'clan_info'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    desc = Column(String)
    khl_server = Column(String)
    qq_group = Column(String)
