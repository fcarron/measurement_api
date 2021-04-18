from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verify_key(X_Secret_Key: str = Header(...)):
    if X_Secret_Key != "1234":
        raise HTTPException(status_code=400, detail="X-Secret-Key invalid")
    return X_Secret_Key


@app.post("/record", response_model=schemas.Record, dependencies=[Depends(verify_key)])
def create_measurement(record: schemas.RecordBase, db: Session = Depends(get_db)):
    record = crud.create_record(db=db, record=record)
    return record


# @app.post("/record", response_model=schemas.Record)
# def create_measurement(record: schemas.RecordBase, db: Session = Depends(get_db)):
#     record = crud.create_record(db=db, record=record)
#     return record


@app.get("/record", response_model=List[schemas.Record])
def get_records(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_records(db=db, skip=skip, limit=limit)


@app.get("/record/{id}", response_model=schemas.Record)
def get_record(id: int, db: Session = Depends(get_db)):
    record = crud.get_record(db=db, id=id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@app.get("/measurement", response_model=List[schemas.Measurement])
def get_measurements(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return crud.get_measurements(db=db, skip=skip, limit=limit)


@app.get("/measurement/{id}", response_model=schemas.Measurement)
def get_measurement(id: int, db: Session = Depends(get_db)):
    measurement = crud.get_measurement(db=db, id=id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return measurement


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
