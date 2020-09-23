

from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import pandas as pd
from db.db_model import DATABASE_URL, Base,  Currency, Saler, Currency_pair
from data_download.download_data import download
datapath = Path(__file__).resolve().parents[1] / "data_download" / "datadir"


engine = create_engine(DATABASE_URL, echo = True)
Session = sessionmaker(bind=engine)
session = Session()




def update_currency() -> bool:

    '''
    Обновляет информацию по валюте из соответствующего файла в data_download/datadir/bm_cy.csv
    Returns:
        True-удача
        False-неудача

    '''
    filename = 'bm_cy.csv'
    data = None
    try:
        data = pd.read_csv(datapath / filename, usecols=[0,1],
                           names=['num', 'name'], delimiter=',')
    except:
        print(f'first need to download a file with currencies')
        return False
    ans = []
    for row in data.values.tolist():
        if not ans:
            ans.append((row[0], row[1]))
        elif (not row[0]  in [x[0] for x in ans]) and (not row[1]  in [x[1] for x in ans]):
            ans.append((row[0], row[1]))
    session.query(Currency).delete()
    for x in ans:
        cur = Currency(num = x[0], name = x[1])
        session.add(cur)
    session.commit()



def update_saler() -> bool:

    '''
    Обновляет информацию по валюте из соответствующего файла в data_download/datadir/bm_exch.csv
    Returns:
        True-удача
        False-неудача

    '''
    filename = 'bm_exch.csv'
    data = None
    try:
        data = pd.read_csv(datapath / filename, usecols=[0,1],
                           names=['num', 'name'], delimiter=',')
    except:
        print(f'first need to download a file with currencies')
        return False
    ans = []
    for row in data.values.tolist():
        if not ans:
            ans.append((row[0], row[1]))
        elif (not row[0]  in [x[0] for x in ans]) and (not row[1]  in [x[1] for x in ans]):
            ans.append((row[0], row[1]))
    session.query(Saler).delete()
    for x in ans:
        cur = Saler(num = x[0], name = x[1])
        session.add(cur)
    session.commit()


# update_currency()
# remove_currency()
# update_currency()

# def update_saler() -> bool:
#     '''
#     Обновляет информацию по продавцу из соответствующего файла в data_download/datadir/0_bm_cy.csv
#     Returns:
#         True-удача
#         False-неудача
#     '''
#
#     pass
#
#
# def make_new_pair() -> bool:
#     '''
#     Обновляет информацию по курсу обмена из файла data_download/datadir/0_bm_exch.csv
#     скачиваем новый пакет данных, пополняем таблицу парой с курсом обмена
#     Returns:
#         True-удача
#         False-неудача
#
#     '''
#     # try:
#     #     download()
#     # except:
#     print(f'скачивание не удалось')
#     pairs = session.query(Currency_pair).all()
#     if len(pairs) <=50:
#         #нужно только вставить
#
#
#         pass
#     elif len(pairs) > 50:
#         #удалить самый давний и вставить новый
#         pass
#     return True
#
#
# def update_data() -> bool:
#     '''
#
#     Returns:
#
#     '''
#     # try:
#         # download()
#     # except:
#     print(f'скачивание не удалось')
#
#
# # make_new_pair()
