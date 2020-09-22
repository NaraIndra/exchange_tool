from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, MetaData

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

# Base = declarative_base()
# metadata = Base.metadata
DATABASE_URL = f"sqlite:///{Path(__file__).parent}/exchange.db"
SECRET_KEY = "1234asdf"

# Base = declarative_base()
# metadata = Base.metadata
#
mymetadata = MetaData()
Base = declarative_base(metadata=mymetadata)


# Base = declarative_base()


class Currency(Base):
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True)
    num = Column(Integer, unique=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)
    # cur_give = relationship('Currency_pair')


class Saler(Base):
    __tablename__ = "saler"
    id = Column(Integer, primary_key=True)
    num = Column(Integer, unique=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)


class Currency_pair(Base):
    __tablename__ = "currency_pair"
    id = Column(Integer, primary_key=True)
    currency_give_id = Column(
        Integer,
        ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID отдаваемой валюты",
    )
    currency_take_id = Column(
        Integer,
        ForeignKey("currency.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID принимаемой валюты",
    )
    saler_id = Column(
        ForeignKey("saler.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID продавца",
    )
    currency_give = relationship("Currency", foreign_keys=[currency_give_id])
    currency_take = relationship("Currency", foreign_keys=[currency_take_id])
    saler = relationship("Saler", foreign_keys=[saler_id])


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
