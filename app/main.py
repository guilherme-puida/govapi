from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
        CORSMiddleware,
        allow_origins=['https://gov.puida.xyz', 'http://gov.puida.xyz'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'])


@app.post("/keyword/", response_model=schemas.Keyword)
def create_keyword(kword: schemas.KeywordCreate, db: Session = Depends(get_db)):
    db_keyword = crud.get_keyword_by_value(db, kword.value)
    if db_keyword:
        raise HTTPException(status_code=400, detail="Keyword with this value already exists")
    new_keyword = crud.create_keyword(db, kword)
    return new_keyword 

@app.get("/keyword/{keyword_id}", response_model=schemas.Keyword)
def get_keyword(keyword_id: int, db: Session = Depends(get_db)):
    db_keyword = crud.get_keyword(db, keyword_id=keyword_id)
    if db_keyword is None:
        return HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@app.get("/keyword/", response_model=list[schemas.Keyword])
def get_keywords(db: Session = Depends(get_db)):
    return crud.get_keywords(db)

@app.get("/page/search/", response_model=schemas.SearchResponse)
def search(q: str, db: Session = Depends(get_db)):
    results = crud.get_pages_containing(db, substr=q)
    return schemas.SearchResponse(count=len(results), results=results)
