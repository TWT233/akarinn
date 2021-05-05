from typing import Optional, List

from sqlalchemy import true
from sqlalchemy.orm import Session

from src.config import *
from src.db import models, schemas


def get(db: Session, game_id: Optional[int] = None, contact_khl: Optional[str] = None,
        contact_qq: Optional[str] = None) -> List[models.Member]:
    cond1 = models.Member.game_id == game_id if game_id else true()
    cond2 = models.Member.contact_khl == contact_khl if contact_khl else true()
    cond3 = models.Member.contact_qq == contact_qq if contact_qq else true()
    return db.query(models.Member).where(cond1, cond2, cond3).all()


def add(db: Session, member: schemas.MemberAdd):
    # check if member exist
    ret = get(db, game_id=member.game_id)
    if len(ret) == 1:
        ret = ret[0]
    elif len(ret) > 1:
        raise ValueError('dup master key?')

    if ret:
        # exists, update member
        entry = ret
        entry.contact_khl = member.contact_khl if member.contact_khl else ''
        entry.contact_qq = member.contact_qq if member.contact_qq else ''
    else:
        # not exists, add new member
        entry = models.Member()
        entry.game_id = member.game_id
        entry.contact_khl = member.contact_khl
        entry.contact_qq = member.contact_qq

    # add high perm level member, check op_key
    if member.permission == models.Member.Permission.VICE_LEADER or \
            member.permission == models.Member.Permission.LEADER:
        if member.op_key != get_op_key():
            return False, {'msg': 'wrong op_key'}

    # set perm
    if member.permission:
        # explicitly set perm in member
        entry.permission = member.permission
    elif not ret:
        # missing perm in member, set default
        entry.permission = models.Member.Permission.MEMBER

    # add entry into db when add new member
    if not ret:
        db.add(entry)

    db.commit()
    return True, entry
