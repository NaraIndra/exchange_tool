import os
import pandas as pd
from typing import Optional, List
from datetime import datetime
from pathlib import Path

datapath = Path(__file__).resolve().parents[1] / "data_download" / "datadir"


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


def gather_init_data():
    ans = []
    for x in os.listdir(datapath):
        print(x)
        if x.split(".")[1] == "csv":
            row = currency_retrieval(datapath / x)
            ans.append(row)
    appended = pd.concat(ans).sort_values(by=["datetime"])
    appended.to_csv("sec.csv")


# gather_init_data()


def currency_find_leader_sec_points(currency_1: int, currency_2: int):
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
        ["cur_give_num", "datetime"]
    ]
    return leader_id, points



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


# currency_find_leader_sec(63, 139)

# for x in os.listdir(datapath):
#     if x.split('.')[1] == 'csv':
#         row = currency_pair_retrieval(datapath / x, cur_give_id, cur_take_id)
#         ans.append(row)
# appended = pd.concat(ans).sort_values(by=['datetime'])
# last_period = appended['datetime'].max()
# min_value = appended['cur_give_num'].min()
# best = appended.loc[(appended['datetime'] == last_period) & (appended['cur_give_num'] == min_value), 'saler_id']
# print(best)
# print(best.values)
# dots = appended.loc[appended['saler_id'] == best.values[0], ['cur_give_num', 'id']]
# dots.plot(x='id', y='cur_give_num')
# print(dots)


# currency_find_leader_sec_points(63, 139)
