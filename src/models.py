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


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


favorite_people = Table(
    "favorite_people",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("people_uid", ForeignKey("people.uid"), primary_key=True)
)

favorite_planets = Table(
    "favorite_planets",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planets_uid", ForeignKey("planets.uid"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    favorites: Mapped[list["People"]] = relationship(
        "People",
        back_populates="favorites",
        secondary=favorite_people
    )
    favoritesP: Mapped[list["Planets"]] = relationship(
        "Planets",
        back_populates="favoritesP",
        secondary=favorite_planets
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
        secondary=favorite_people
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
    favoritesP: Mapped[list["User"]] = relationship(
        "User",
        back_populates="favoritesP",
        secondary=favorite_planets
    )

    def __init__(planet, name, description):
        planet.name = name
        planet.description = description
        db.session.add(planet)
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
