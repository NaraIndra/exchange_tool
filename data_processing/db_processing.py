import time
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
            datapath / filename, usecols=[0, 1], names=["id", "name"], delimiter=","
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
    pairs['datetime'] =  pd.to_datetime(pairs['datetime'])
    # print(pairs.dtypes)
    count = db.session.query(Currency_pair).distinct(Currency_pair.datetime).count()
    print(count)
    if count < 50:
        start_time = time.time()
        pairs = pairs.values.tolist()
        ans = []
        for pair in pairs:
            # print(pair[0], pair[1])
            cur_give = db.session.query(Currency.id).filter(Currency.num == pair[0]).all()[0][0]
            cur_take = db.session.query(Currency.id).filter(Currency.num == pair[1]).all()[0][0]
            sale = db.session.query(Saler.id).filter(Saler.num == pair[2]).all()[0][0]
            pair_tuple = Currency_pair(
                currency_give_id=cur_give,
                currency_take_id=cur_take,
                saler_id=sale,
                amount_give=pair[3],
                amount_take=pair[4],
                volume=pair[5],
                datetime=pair[6],
            )
            ans.append(pair_tuple)
        db.session.add_all(ans)
        db.session.commit()
        data = db.session.query(Currency_pair).all()
        # print(data)
        print('!!!', len(data))
        print(f'! {time.time() - start_time}, {count}')
    # elif count >= 50:
    #     # удалить самый давний и вставить новый
    #     pass
    # return True

# a = Currency_pair.query.limit(100)
# print([x.currency_give_id for x in a])
# make_new_pair()


def update_data() -> bool:
    """
    обновляет данные всех трех таблиц, скачивая архив из ресурса

    Returns:
    """
    # try:
    # download()
    # except:
    try:
       download()
       update_currency()
       update_saler()
       make_new_pair()

    except:
        print(f"скачивание не удалось")


update_data()

