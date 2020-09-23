import requests
from zipfile import ZipFile
import csv
from pathlib import Path

url = "http://api.bestchange.ru/info.zip"
path = Path(__file__).parent
zippath = path.parent / "download" / "zipdir"
infopath = path / 'info'
zipfilepath = ""

Path(path.parent /  "download"  / "zipdir").mkdir(parents=True, exist_ok=True)
Path(path / "info").mkdir(parents=True, exist_ok=True)

def reformat_info_data():
    with open(zippath / 'bm_cy.dat', encoding = "ISO-8859-1") as dat_file, open(infopath / 'id_currency.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in dat_file:
            uline = line.encode('utf-8').decode('utf-8')
            row = [field.strip() for field in uline.split(';')]
            if len(row) == 7 and row[3] and row[4]:
                if ('Tether' in row[2]):
                    print(row[0], row[2])
                csv_writer.writerow([row[0] + ';' + row[2]])

reformat_info_data()

