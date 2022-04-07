from pydantic import BaseModel

class PageBase(BaseModel):
    url: str
    visited: bool

    heading: str | None
    description: str | None
    body: str | None

class Page(PageBase):
    id: int

    class Config:
        orm_mode = True


class KeywordBase(BaseModel):
    value: str

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: int

    class Config:
        orm_mode = True 


class SearchResponse(BaseModel):
    count: int
    results: list[Page] = []

    class Config:
        orm_mode = True
