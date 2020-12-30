from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey, Table

Base = declarative_base()

"""
one to one
one to many -> many to one
many to many
"""

tag_post = Table(
    "tag_post",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, unique=False, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")
    tags = relationship("Tag", secondary=tag_post, back_populates="posts")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, unique=False, nullable=False)
    posts = relationship("Post")
    comment = relationship("Comment")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, unique=False, nullable=False)
    posts = relationship("Post", secondary=tag_post)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    parent = relationship("Comment")
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author")