
import os
import requests
import csv
from zipfile import ZipFile
from pathlib import Path
from datetime import datetime
from shutil import copyfile
from data_download.util.cleaner import cleaner
from data_download.util.dat2csv_converter import dat_to_csv_converter

url = "http://api.bestchange.ru/info.zip"
path = Path(__file__).parent
zippath = path / "zipdir"
datapath = path / "datadir"
datapandaspath = path / 'datapandasdir'

Path(path / "zipdir").mkdir(parents=True, exist_ok=True)
Path(path / 'datadir').mkdir(parents=True, exist_ok=True)
Path(path / 'datapandasdir').mkdir(parents=True, exist_ok=True)


from data_download.util.cleaner import cleaner
from data_download.util.dat2csv_converter import dat_to_csv_converter


filename = ""

if url.find("/"):
    filename = url.rsplit("/", 1)[1]
    filepath = path / filename
else:
    filepath = path / "info.zip"


def download() -> datetime:
    '''
    Загружает данные единожды
    Returns: успех завершения операции

    '''
    filename = ""
    time = None
    if url.find("/"):
        filename = url.rsplit("/", 1)[1]
        zipfilepath = zippath / filename
    else:
        zipfilepath = zippath / "info.zip"
    r = requests.get(url, allow_redirects=True)
    print(r)
    if not r:
        print("bad_request")
        return False
    try:
        open(f"{zipfilepath}", "wb").write(r.content)
        with ZipFile(zipfilepath, "r") as zipObj:
            a = zipObj.extractall(zippath)
        for file in os.listdir(zippath):
            if ".dat" in  file:
                # os.rename(zippath / file, zippath / f"0_{file}")
                time = dat_to_csv_converter(f"{file}")
        for file in os.listdir(datapath):
            print(file)
            copyfile(datapath / file, datapandaspath / file)
            new_filename = file[:-4] + '_new.csv'
            os.rename(datapandaspath / file, datapandaspath / new_filename)
        cleaner("dat")
        return time
    except Exception as e:
        print(e)

download()

def downloader():
    '''
    Вечный цикл загрузки
    Returns:

    '''
    while True:
        download()

def download_k_times(k: int):
    '''
    загружает k пакетов с данными, преобразовывает их в формат csv и сохраняет в папке 'datedir'
   
    Args:
       k: количество загрузок

    Returns:

    '''
    for i in range(k):
        try:
            r = requests.get(url, allow_redirects=True)
            open(path / filename, "wb").write(r.content)
            with ZipFile(path / filename, "r") as zipObj:
                a = zipObj.extractall(zippath)
                for file in os.listdir(zippath):
                    if "bm_rates.dat" == file:
                        # os.rename(zippath / file, zippath / f"{i}_{file}")
                        dat_to_csv_converter(f"{i}_{file}")
                cleaner("dat")
            os.remove(os.path.join(path, 'info.zip'))


        except:
            print("bad_request")


# download_k_times(100)
