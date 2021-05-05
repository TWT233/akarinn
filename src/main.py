from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import models, crud, schemas
from .db.init import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.get('/', response_model=schemas.StatusRetSucc)
# async def root(db: Session = Depends(get_db)):
#     crud_res = crud.get_status(db)
#     return schemas.StatusRetSucc(status=crud_res)


@app.get('/status', response_model=schemas.StatusRet)
async def status_get(db: Session = Depends(get_db)):
    return crud.status.get(db)


@app.post('/battle/log', response_model=schemas.BattleLogRet)
async def battle_log_post(commit: schemas.BattleLogCommit, db=Depends(get_db)):
    status, ret = crud.battle_log.commit(db, commit)
    if not status:
        raise HTTPException(403, ret)
    return schemas.BattleLogRet(log=ret, status=crud.status.get(db))


@app.get('/member', response_model=List[schemas.Member])
async def member_get(game_id: int = None, contact_khl: str = None, contact_qq: str = None, db=Depends(get_db)):
    return crud.member.get(db, game_id=game_id, contact_khl=contact_khl, contact_qq=contact_qq)


@app.post('/member', response_model=schemas.Member)
async def member_post(member: schemas.MemberAdd, db=Depends(get_db)):
    status, ret = crud.member.add(db, member)
    if not status:
        raise HTTPException(403, ret)
    return ret
    # test data:
# {
# "game_id": 524871626,
# "contact_khl": "aaaaaaaaaaa",
# "contact_qq": "549218202",
# "permission": 0,
# "op_key": "b8f3d59faf4a0e70"
# }

# @app.get('/battle/log', response_model=List[schemas.BattleLog])
# async def battle_log(response: Response,
#                      who: Optional[str] = None,
#                      which_day: Optional[Union[datetime.date, str]] = None,
#                      db=Depends(get_db)):
#     which_day = get_real_which_day(which_day)
#     if not which_day:
#         response.status_code = 400
#         return {'message': 'wrong param'}
#     return crud.get_battle_logs(db, who=who, which_day=which_day)

# @app.get('/battle/log/count')
# async def battle_log_count(response: Response,
#                            who: Optional[str] = None,
#                            which_day: Optional[Union[datetime.date, str]] = None,
#                            db=Depends(get_db)):
#     which_day = get_real_which_day(which_day)
#     if not which_day:
#         response.status_code = 400
#         return {'message': 'wrong param'}
#     return crud.count_battles(db, who=who, which_day=which_day)
