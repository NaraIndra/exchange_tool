import time
from sqlalchemy import func, distinct, tuple_
from sqlalchemy.exc import SQLAlchemyError
from pathlib import Path
import pandas as pd
from db.db_model import db, Currency, Saler, Currency_pair
from data_download.download_data import download
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from globals import (
    minute2_datetime_label_g,
    minute10_datetime_label_g,
    hour_datetime_label_g,
    day_datetime_label_g,
)

datapath = Path(__file__).resolve().parents[1] / "data_download" / "datadir"


# engine = create_engine(DATABASE_URL, echo=True)
# Session = sessionmaker(bind=engine)
# session = Session()


def update_currency(session: db.session) -> bool:

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
    ans = []
    # нет проверки на уникальность номеров
    for row in data.values.tolist():
        ans.append(Currency(num=row[0], name=row[1]))
    session.query(Currency).delete()
    try:
        session.add_all(ans)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()


def update_saler(session: db.session) -> bool:

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
    # нет проверки на уникальность номеров
    for row in data.values.tolist():
        ans.append(Saler(num=row[0], name=row[1]))
    session.query(Saler).delete()
    try:
        session.add_all(ans)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()


def make_new_pair(
    session: db.session, minute2: bool, minute10: bool, hour: bool, day: bool
) -> bool:
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
    pairs["datetime"] = pd.to_datetime(pairs["datetime"])
    count = (
        db.session.query(Currency_pair.datetime)
        .distinct(Currency_pair.datetime)
        .count()
    )
    print(count)
    if count < 4:
        # start_time = time.time()
        pairs = pairs.values.tolist()
        ans = []
        for pair in pairs:
            pair_tuple = Currency_pair(
                cur_give_num=pair[0],
                cur_take_num=pair[1],
                saler_num=pair[2],
                amount_give=pair[3],
                amount_take=pair[4],
                volume=pair[5],
                datetime=pair[6],
            )
            ans.append(pair_tuple)
        db.session.add_all(ans)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
    elif count >= 4:
        try:
            min_date = (
                db.session.query(Currency_pair.datetime)
                .distinct(Currency_pair.datetime)
                .order_by("datetime")
                .limit(1)
                .all()
            )
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
        try:
            db.session.query(Currency_pair).filter(
                Currency_pair.datetime == min_date[0][0]
            ).delete()
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()


count = 0


def update_data(session: db.session, sched: BackgroundScheduler) -> bool:
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
        update_currency(session)
        update_saler(session)
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
