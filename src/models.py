from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    String, Column, Table, ForeignKey
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    mapped_column, relationship,
)

db = SQLAlchemy()


class Base(DeclarativeBase):
    pass


favorite_table = Table(
    "favorite_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("people_uid", ForeignKey("people.uid"), primary_key=True)
)


# class Favorites(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    favorites: Mapped[list["People"]] = relationship(
        "People",
        back_populates="favorites",
        secondary=favorite_table
    )

    def __init__(self, email):
        self.email = email
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People (db.Model):
    __tablename__ = "people"
    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(120), nullable=False)
    favorites: Mapped[list["User"]] = relationship(
        "User",
        back_populates="favorites",
        secondary=favorite_table
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }


class Planets (db.Model):
    uid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(120), nullable=False)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }
