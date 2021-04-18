from sqlalchemy.orm import Session

from . import models, schemas


def create_record(db: Session, record: schemas.RecordBase):
    db_record = models.Record(time=record.time)
    for m in record.measurement:
        db_record.measurement.append(
            models.Measurement(type=m.type, value=m.value, place=m.place)
        )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def get_record(db: Session, id: int):
    return db.query(models.Record).filter(models.Record.id == id).first()


def get_records(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Record)
        .order_by(
            models.Record.id.desc(),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_measurements(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Measurement)
        .order_by(models.Measurement.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_measurement(db: Session, id: int):
    return db.query(models.Measurement).filter(models.Measurement.id == id).first()
