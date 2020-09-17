from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship

DATABASE_URL= f'sqlite:///{Path(__file__).parent}/exchange.db'
SECRET_KEY = '1234asdf'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)

class Saler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(30), unique=True, nullable=False)

class Pair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_give_id = Column(
        Integer,
        ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID отдаваемой валюты",
    )
    currency_give = relationship("Currency", foreign_keys=[currency_give_id],  back_populates="currency")
    currency_take_id = Column(
        Integer,
        ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID принимаемой валюты",
    )
    currency_take = relationship("Currency", foreign_keys=[currency_take_id],  back_populates="currency")
    saler_id = Column(
        ForeignKey("saler.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID продавца",
    )
    saler = relationship("Saler", foreign_keys=[saler_id],  back_populates="saler")
