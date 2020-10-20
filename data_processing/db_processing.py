import time
from sqlalchemy import func, distinct, tuple_
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
import pandas as pd
from db.db_model import Currency, Saler, Currency_pair
from data_download.download_data import download
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sm import db
import os
from shutil import copyfile
from globals import (
    minute2_datetime_label_g,
    minute10_datetime_label_g,
    hour_datetime_label_g,
    day_datetime_label_g,
)

datapath = Path(__file__).resolve().parents[1] / "data_download" / "datadir"
datapandaspath = Path(__file__).resolve().parents[1] / "data_download" / "datapandasdir"

# engine = create_engine(DATABASE_URL, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()


def update_currency_pandas() -> bool:

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
            datapath / filename, usecols=[0, 2], names=["num", "name"], delimiter=","
        )
    except:
        print(f"first need to download a file with currencies")
        return False
    copyfile(datapath / filename, datapandaspath / 'db_currency.csv')


def update_saler_pandas() -> bool:

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
    copyfile(datapath / filename, datapandaspath / 'db_saler.csv')




def make_new_pair_pandas(
        minute2: bool, minute10: bool, hour: bool, day: bool
) -> bool:
    """
    Обновляет информацию по курсу обмена из файла data_download/datadir/0_bm_exch.csv
    скачиваем новый пакет данных, пополняем таблицу парой с курсом обмена
    Returns:
        True-удача
        False-неудача

    """
    filename = "bm_rates.csv"
    db_filename = datapandaspath / 'db_pairs_sec.csv'
    pairs = None
    db = None
    try:
        db = pd.read_csv(
            datapandaspath / db_filename,
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
        copyfile(datapath / filename, datapandaspath / db_filename)
        return
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
            index = [i for i in ]
            )
    except:
        print(f"first need to download a file with currencies")
        return

    ans = []

    db.reset_index(drop=True, inplace=True)
    pairs.reset_index(drop=True, inplace=True)

    res = pd.concat([db, pairs], axis=0)
    count = db.datetime.nunique()
    print(res.shape)
    print(count)
    if count > 30:
        min_date = res.datetime.min()
        res.drop(res[res.datetime == min_date].index, inplace = True)
    res.to_csv(db_filename)

make_new_pair_pandas(None, None, None, None)

def update_data_pandas(session: db.session, sched: BackgroundScheduler) -> bool:
    """
    обновляет данные всех трех таблиц, скачивая архив из ресурса

    Returns:
    """
    time = None
    global count
    global minute2_datetime_label_g
    global minute10_datetime_label_g
    global hour_datetime_label_g
    global day_datetime_label_g
    sched.print_jobs()
    print("Count: ", count)
    count += 1
    # start_time = time.time()
    try:
        time = download()
    except Exception as e:
        print(e)
    need_update_minute_2 = process_minute2_timer(time)
    need_update_minute_10 = process_minute10_timer(time)
    try:
        update_currency_pandas()
        update_saler_pandas()
        make_new_pair_pandas(
            need_update_minute_2, need_update_minute_10, False, False
        )
    except Exception as e:
        print(e)
    print("Count: ", count)
    current = session.query(Currency_pair.datetime).order_by(Currency_pair.datetime)

    # print(f"! {time.time() - start_time}")

def update_data_1(sched: BackgroundScheduler) -> bool:
    """
    обновляет данные всех трех таблиц, скачивая архив из ресурса

    Returns:
    """
    time = None
    global count
    global minute2_datetime_label_g
    global minute10_datetime_label_g
    global hour_datetime_label_g
    global day_datetime_label_g
    sched.print_jobs()
    print("Count: ", count)
    count += 1
    # start_time = time.time()
    try:
        time = download()
    except Exception as e:
        print(e)
    need_update_minute_2 = process_minute2_timer(time)
    need_update_minute_10 = process_minute10_timer(time)
    try:
        #update_currency(session)
        #update_saler(session)
        make_new_pair(
            session, need_update_minute_2, need_update_minute_10, False, False
        )
    except Exception as e:
        print(e)
    print("Count: ", count)
    current = session.query(Currency_pair.datetime).order_by(Currency_pair.datetime)

    # print(f"! {time.time() - start_time}")

def process_minute2_timer(time: datetime) -> bool:
    """
    обновляет глобальный 2минутный таймер при необходимости и сообщает о необходимости внести
    в базу изменения
    Args:
        time: время крайней закачки архива

    Returns: True-необходимо внести инфу в базу False-нет

    """
    global minute2_datetime_label_g
    if not minute2_datetime_label_g:
        minute2_datetime_label_g = time
        return True
    elif time.minute - minute2_datetime_label_g.minute >= 2:
        minute2_datetime_label_g = time
        return True
    else:
        return False


def process_minute10_timer(time: datetime) -> bool:
    """
    обновляет глобальный 2минутный таймер при необходимости и сообщает о необходимости внести
    в базу изменения
    Args:
        time: время крайней закачки архива

    Returns: True-необходимо внести инфу в базу, False-нет

    """
    global minute10_datetime_label_g
    if not minute10_datetime_label_g:
        minute10_datetime_label_g = time
        return True
    elif time.minute - minute10_datetime_label_g.minute >= 2:
        minute10_datetime_label_g = time
        return True
    else:
        return False
