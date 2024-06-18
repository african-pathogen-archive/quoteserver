# import json
import os
import os.path

from contextlib import asynccontextmanager
from random import randint
from sys import stderr

from fastapi import FastAPI, Query, HTTPException, Depends
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import select, func

from models import *

description = """
Quotes API for when you need a little inspiration.
"""

appconfig = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT', "5432")
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # if db_url is not None and db_user is not None and db_password is not None:
    # db_url = f'sqlite:///{os.path.dirname(__file__)}/../data/quotes.db'
    db_url = f'postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(db_url)
    # engine = create_engine(db_url, connect_args={"check_same_thread": False})
    # engine = create_engine(db_url, connect_args={"check_same_thread": False})
    appconfig['engine'] = engine
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="QuotesAPI", description=description, lifespan=lifespan)

def get_session():
    engine = appconfig['engine']
    with Session(engine) as session:
        yield session

# data_dir = os.environ.get('DATA_PATH', os.path.dirname(__file__) + '/../data')
# quotes = json.load(open(data_dir + '/quotes.json'))
# max_id = len(quotes)

@app.get("/")
async def root():
    return {"status": "live"}


@app.get("/quote/", response_model=QuotePublicWithSourceAndAuthors)
async def get_quote(quote_id: int = Query(-1, description="The ID of the quote you want to retrieve. Leave blank to get a random quote."),
                    session: Session = Depends(get_session)):
    if quote_id == -1:
        query = select(func.max(Quote.id))
        max_id = session.exec(query).scalar()
        if max_id is None:
            raise HTTPException(status_code=404, detail="No quotes found.")
        quote_id = randint(1, max_id)

    query = select(Quote).where(Quote.id == quote_id)
    quote = session.scalars(query).first()
    if quote is None:
        raise HTTPException(status_code=404, detail=f"Quote not found: {quote_id}")
    return quote

@app.get("/quote/all", response_model=list[QuotePublic])
async def get_quotes(session: Session = Depends(get_session)):
    query = select(Quote)
    quotes = session.exec(query).scalars().all()
    return quotes


@app.post("/quote/", response_model=QuotePublic)
async def put_quote(quote: QuoteCreate, session: Session = Depends(get_session)):
    db_quote = Quote.model_validate(quote)
    session.add(db_quote)
    session.commit()
    session.refresh(db_quote)
    return db_quote

@app.post("/source/", response_model=SourcePublic)
async def put_source(source: SourceCreate, session: Session = Depends(get_session)):
    db_source = Source.model_validate(source)
    session.add(db_source)
    session.commit()
    session.refresh(db_source)
    return db_source

@app.post("/author/", response_model=AuthorPublic)
async def put_author(author: AuthorCreate, session: Session = Depends(get_session)):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@app.get("/source/all", response_model=list[SourcePublic])
async def get_sources(session: Session = Depends(get_session)):
    query = select(Source)
    sources = session.exec(query).scalars().all()
    print(dict(sources[0]))
    return sources

@app.get("/author/all", response_model=list[AuthorPublic])
async def get_authors(session: Session = Depends(get_session)):
    query = select(Author)
    authors = session.exec(query).all()
    return authors
