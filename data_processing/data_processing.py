import os
import pandas as pd
from typing import Optional, List
from pathlib import Path


from sqlalchemy import create_engine, MetaData, func, desc, DateTime
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import pandas as pd
from datetime import datetime
from db.db_model import Currency, Saler, Currency_pair
from sm import db
from data_download.download_data import download
from data_processing.utils.utils import find_minvalue_from_list

datapath = Path(__file__).resolve().parents[1] / "data_download" / "datadir"

#
# engine = create_engine(DATABASE_URL, echo = True)
# Session = sessionmaker(bind=engine)
# session = Session()

print(db, dir(db))

def currency_retrieval(filename) -> Optional[pd.DataFrame]:

    """
    возвращает dataframe с соответствующими валютами, извлеченный из файла
    Args:
        filename: имя файла
        cur_1: валюта, которую мы отдает
        cur_2: валюта, которую мы получаем

    Returns: dataframe с информацией о валютной паре

    """
    data_new = pd.read_csv(
        filename,
        sep=",",
        names=[
            "cur_give_id",
            "cur_take_id",
            "saler_id",
            "cur_give_num",
            "cur_take_num",
            "volume",
            "datetime",
        ],
    )
    # row = data_new[(data_new.cur_give_id == cur_1) & (data_new.cur_take_id == cur_2)]
    return data_new

def find_cp_last_datetime(currency_give_num: int, currency_take_num: int) -> Optional[datetime]:
    '''
    Находит последнюю дату записи в таблице Currency_pair
    Args:
        currency_give_num: номер отдаваемой валюты
        currency_take_num: номер получаемой валюты

    Returns: дата последней заключенной сделке по данной валюте

    '''
    last_time = None
    try:
        last_time = db.session.query(Currency_pair.datetime)\
        .filter(Currency_pair.cur_give_num == currency_give_num, Currency_pair.cur_take_num == currency_take_num)\
        .order_by(desc('datetime')).limit(1).all()
        print('11111', last_time)
        n = db.session.query(Currency_pair.datetime).all()
        print(len(n))
    except Exception as e:
        raise

    return last_time[0][0]

def pair_find_leader(currency_give_num: int, currency_take_num: int, last_datetime: datetime) -> Optional[int]:
    '''
    находит лидера по последней записи в бд currency_pair
    Args:
        currency_give_num:номер отдаваемой валюты
        currency_take_num:номер получаемой валюты

    Returns:номер обменника, в котором количество отдаваемой валюты
    за получаемую валюту наименьшее
    '''
    data = db.session.query(Currency_pair).filter(
            Currency_pair.cur_give_num == currency_give_num,
            Currency_pair.cur_take_num == currency_take_num,
            Currency_pair.datetime == last_datetime
            ).all()
    if not len(data):
        print('shit')
        return  None
    #здесь вытягиваю список для проверки, нужное значение - saler_num
    #переделать с df на обычный список
    min_value_saler_num = find_minvalue_from_list(data)
    return min_value_saler_num

def find_cp_leaderpoints_minutes(leader_num: int, last_datetime: DateTime,
                                 currency_give: int, currency_take: int) -> Optional[List[float]]:
    '''
    Возвращает список значений количества отданной валюты у наиболее дешевого обменника
    Args:
        leader_num: номер лидера

    Returns:список флотов(количество отдаваемой валюты в промежутке 1 часа(30 точек))
    '''
    print(leader_num, currency_take, currency_give)
    try:
        data = pd.read_sql(
            db.session.query(Currency_pair.datetime, Currency_pair.amount_give)
                .filter(
                Currency_pair.cur_give_num == currency_give,
                Currency_pair.cur_take_num == currency_take,
                Currency_pair.saler_num == leader_num
            )
                .statement,
            db.session.bind
        )
    except:
        print(f'no such pair in db: {currency_give=}, {currency_take=}')
        return None
    return data


def currency_find_leader_sec_points(currency_1: int, currency_2: int):
    """
    Нахождение секундного лидера
    Args:
        # cur_give_id: валюта, которую отдаем
        # cur_take_id: валюта, которую получаем

    Returns:

    """
    # data = pd.read_csv("sec.csv")
    data = pd.read_sql(
        db.session.query(Currency_pair)
        .filter(
            Currency_pair.cur_give_num == currency_1,
            Currency_pair.cur_take_num == currency_2,
        )
        .statement,
        db.session.bind,
    )
    print(data)
    if not data:
        return None, []
    last_period = data["datetime"].max()
    best = data.loc[
        (data["cur_give_num"] == currency_1) &
        (data["cur_take_num"] == currency_2) &
        (data["datetime"] == last_period)
    ]
    leader_num = best.loc[
        (best["cur_give_num"] == best["cur_give_num"].min()), "saler_num"
    ].values[0]
    points = data.loc[
        (data["saler_num"] == leader_num)
        & (data["cur_give_num"] == currency_1)
        & (data["cur_take_num"] == currency_2),
        ["amount_give", "datetime"],
    ]
    return leader_num, points


def currency_find_leader_10sec_points(currency_1: int, currency_2: int):
    """
    Нахождение секундного лидера
    Args:
        # cur_give_id: валюта, которую отдаем
        # cur_take_id: валюта, которую получаем

    Returns:

    """
    data = pd.read_csv("sec.csv")
    last_period = data["datetime"].max()
    best = data.loc[
        (data["cur_give_id"] == currency_1)
        & (data["cur_take_id"] == currency_2)
        & (data["datetime"] == data["datetime"].max()),
    ]
    leader_id = best.loc[
        (best["cur_give_num"] == best["cur_give_num"].min()), "saler_id"
    ].values[0]
    points = data.loc[
        (data["saler_id"] == leader_id)
        & (data["cur_give_id"] == currency_1)
        & (data["cur_take_id"] == currency_2),
        "cur_give_num",
    ]
    return leader_id, points


def retrive_leader_points_sec(currency_give: int, currency_take: int, leader: int):

    pass
