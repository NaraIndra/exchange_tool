from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import pandas as pd
from db.db_model import db, Currency, Saler, Currency_pair
from data_download.download_data import download

datapath = Path(__file__).resolve().parents[1] / "data_download" / "datadir"


# engine = create_engine(DATABASE_URL, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()


def update_currency() -> bool:

    """
    Обновляет информацию по валюте из соответствующего файла в data_download/datadir/bm_cy.csv
    Returns:
        True-удача
        False-неудача

    """
    filename = "bm_cy.csv"
    data = None
    try:
        data = pd.read_csv(
            datapath / filename, usecols=[0, 1], names=["num", "name"], delimiter=","
        )
    except:
        print(f"first need to download a file with currencies")
        return False
    ans = []
    for row in data.values.tolist():
        if not ans:
            ans.append((row[0], row[1]))
        elif (not row[0] in [x[0] for x in ans]) and (
            not row[1] in [x[1] for x in ans]
        ):
            ans.append((row[0], row[1]))
    db.session.query(Currency).delete()
    for x in ans:
        cur = Currency(num=x[0], name=x[1])
        db.session.add(cur)
    db.session.commit()


def update_saler() -> bool:

    """
    Обновляет информацию по валюте из соответствующего файла в data_download/datadir/bm_exch.csv
    Returns:
        True-удача
        False-неудача

    """
    filename = "bm_exch.csv"
    data = None
    try:
        data = pd.read_csv(
            datapath / filename, usecols=[0, 1], names=["num", "name"], delimiter=","
        )
    except:
        print(f"first need to download a file with currencies")
        return False
    ans = []
    for row in data.values.tolist():
        if not ans:
            ans.append((row[0], row[1]))
        elif (not row[0] in [x[0] for x in ans]) and (
            not row[1] in [x[1] for x in ans]
        ):
            ans.append((row[0], row[1]))
    db.session.query(Saler).delete()
    for x in ans:
        cur = Saler(num=x[0], name=x[1])
        db.session.add(cur)
    db.session.commit()


def make_new_pair() -> bool:
    """
    Обновляет информацию по курсу обмена из файла data_download/datadir/0_bm_exch.csv
    скачиваем новый пакет данных, пополняем таблицу парой с курсом обмена
    Returns:
        True-удача
        False-неудача

    """
    filename = "bm_rates.csv"
    pairs = None
    try:
        pairs = pd.read_csv(
            datapath / filename,
            usecols=[0, 1, 2, 3, 4, 5, 8],
            names=[
                "cur_give_id",
                "cur_take_id",
                "saler_id",
                "amount_give",
                "amount_take",
                "volume",
                "datetime",
            ],
            delimiter=",",
        )
    except:
        print(f"first need to download a file with currencies")
        return False
    ans = []
    print(pairs)
    # db_pairs = session.query()
    count = db.session.query(Currency_pair).distinct(Currency_pair.datetime).count()

    if count < 50:
        pairs = pairs.values.tolist()
        for pair in pairs:
            pair = Currency_pair(
                currency_give_id=pair[0],
                currency_take_id=pair[1],
                saler_id=pair[2],
                amount_give=pair[3],
                amount_take=pair[4],
                volume=pair[5],
                datetime=pair[6],
            )
            db.session.add(pair)
        db.session.commit()
    elif count >= 50:
        # удалить самый давний и вставить новый
        pass
    return True


make_new_pair()


def update_data() -> bool:
    """

    Returns:

    """
    # try:
    # download()
    # except:
    print(f"скачивание не удалось")


# make_new_pair()
