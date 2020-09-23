from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import pandas as pd
from db.db_model import DATABASE_URL, Base,  Currency, Saler
from sqlalchemy import inspect

engine = create_engine(DATABASE_URL, echo = True)
# Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

print(Base.metadata)

def populate_currency():
    csv_data = pd.read_csv("id_currency.csv", delimiter=";")
    csv_data = csv_data.values.tolist()
    ans = []
    for row in csv_data:
        if not ans:
            ans.append((row[0], row[1]))
        elif (not row[0]  in [x[0] for x in ans]) and (not row[1]  in [x[1] for x in ans]):
            ans.append((row[0], row[1]))
    for x in ans:
        cur = Currency(num = x[0], name = x[1])
        session.add(cur)
    session.commit()


def populate_saler():
    csv_data = pd.read_csv("id_saler.csv", delimiter=",")
    csv_data = csv_data.values.tolist()
    ans = []
    for row in csv_data:
        if not ans:
            ans.append((row[0], row[1]))
        elif (not row[0]  in [x[0] for x in ans]) and (not row[1]  in [x[1] for x in ans]):
            ans.append((row[0], row[1]))
    for x in ans:
        saler = Saler(num = x[0], name = x[1])
        session.add(saler)
    session.commit()
