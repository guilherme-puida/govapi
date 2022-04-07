from sqlalchemy.orm import Session

from . import models, schemas


def get_page(db: Session, page_id: int):
    return db.query(models.Page).filter(models.Page.id == page_id).first()


def get_pages_containing(db: Session, substr: str):
    query = f"%{substr}%"
    return db.query(models.Page).filter(
        (
            (models.Page.heading.ilike(query))
            | (models.Page.description.ilike(query))
            | (models.Page.body.ilike(query))
        )
    ).all()


def create_keyword(db: Session, keyword: schemas.KeywordCreate):
    db_keyword = models.Keyword(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)

    return db_keyword

def get_keyword(db: Session, keyword_id: int):
    return db.query(models.Keyword).filter(models.Keyword.id == keyword_id).first()

def get_keywords(db: Session):
    return db.query(models.Keyword).all()

def get_keyword_by_value(db: Session, kword: str):
    return db.query(models.Keyword).filter(models.Keyword.value == kword).first()

