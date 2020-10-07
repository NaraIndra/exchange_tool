from pathlib import Path
from sqlalchemy.orm import relationship
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
    DateTime,
    UniqueConstraint,
    text,
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_URL = f"sqlite:///{Path(__file__).parent}/exchange.db"
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#эта хрень нужна потому что по внешние ключи в sqlite не слушаются
#(дефолтное неслушание внешних ключей сделано для
#обратной совместимости в рамках sqlite)
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
    def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
        dbapi_con.execute('pragma foreign_keys=ON')


    with app.app_context():
        from sqlalchemy import event

        event.listen(db.engine, 'connect', _fk_pragma_on_connect)


class Currency(db.Model):
    __tablename__ = "currency"
    id = Column(Integer, nullable=False, primary_key=True)
    num = Column(Integer, unique=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)


class Saler(db.Model):
    __tablename__ = "saler"
    id = Column(Integer, nullable=False, primary_key=True)
    num = Column(Integer, unique=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)


class Currency_pair(db.Model):
    __tablename__ = "currency_pair"
    id = Column(Integer, nullable = False, primary_key=True)
    cur_give_num = Column(Integer, index = True, nullable = False)
    cur_take_num = Column(Integer, index = True, nullable = False)
    saler_num = Column(Integer, index = True, nullable = False)
    amount_give = Column(Integer, index = True, nullable=False)
    amount_take = Column(Integer, index = True, nullable=False)
    volume = Column(Integer, index = True, nullable=False)
    datetime = Column(DateTime, index = True, unique=False)

    def __repr__(self):
        return f'{self.id=}\n{self.cur_give_num=}\n{self.cur_take_num=}' \
               f'{self.amount_give=}\n{self.amount_take=}\n{self.volume=}'\
               f'{self.datetime}'

# db.drop_all()
db.create_all()
