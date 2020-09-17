from datetime import datetime
import csv
from pathlib import Path


def dat_to_csv_converter(filename):
    zippath = Path(__file__).resolve().parents[1] / 'zipdir'
    datapath = Path(__file__).resolve().parents[1] / 'datadir'
    new_filename = filename[:-3] + 'csv'
    with open(zippath / filename, encoding="ISO-8859-1") as dat_file, open(
            datapath / new_filename, "w+"
    ) as csv_file:
        csv_writer = csv.writer(csv_file)
        time = datetime.now()
        for line in dat_file:
            uline = line.encode("utf-8").decode("utf-8")
            row = [field.strip() for field in uline.split(";")]
            row = row[0:6]
            row.append(time)
            csv_writer.writerow(row)
