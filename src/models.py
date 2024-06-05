from sqlmodel import SQLModel, Field, Relationship

# class SourceQuoteLink(SQLModel, table=True):
#     __tablename__ = "source_quote_link"
#     source_id: int = Field(default=None, foreign_key="sources.id", primary_key=True)
#     quote_id: int = Field(default=None, foreign_key="quotes.id", primary_key=True)


class SourceBase(SQLModel):
    name: str
    date: int

class Source(SourceBase, table=True):
    __tablename__ = "sources"
    id: int | None = Field(default=None, primary_key=True)
    quotes: list["Quote"] = Relationship(back_populates="source")

class SourceCreate(SourceBase):
    pass

class SourcePublic(SourceBase):
    id: int

class AuthorQuoteLink(SQLModel, table=True):
    __tablename__ = "author_quote_link"
    author_id: int = Field(default=None, foreign_key="authors.id", primary_key=True)
    quote_id: int = Field(default=None, foreign_key="quotes.id", primary_key=True)

class AuthorBase(SQLModel):
    name: str

class Author(AuthorBase, table=True):
    __tablename__ = "authors"
    id: int | None = Field(default=None, primary_key=True)
    quotes: list["Quote"] = Relationship(back_populates="authors", link_model=AuthorQuoteLink)

class AuthorCreate(AuthorBase):
    pass

class AuthorPublic(AuthorBase):
    id: int

class QuoteBase(SQLModel):
    quote: str
    source_id: int | None = Field(default=None, foreign_key="sources.id")

class Quote(QuoteBase, table=True):
    __tablename__ = "quotes"
    id: int | None = Field(default=None, primary_key=True)
    source: Source | None = Relationship(back_populates="quotes")
    authors: list[Author] = Relationship(back_populates="quotes", link_model=AuthorQuoteLink)

class QuoteCreate(QuoteBase):
    pass

class QuotePublic(QuoteBase):
    id: int

class QuotePublicWithSourceAndAuthors(QuotePublic):
    id: int
    source: SourcePublic
    authors: list[AuthorPublic]