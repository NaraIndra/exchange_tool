import requests
from zipfile import ZipFile
from pathlib import Path

url = "http://api.bestchange.ru/info.zip"
path = Path(__file__).parent
zippath = path / "zipdir"
zipfilepath = ""

Path(path / "zipdir").mkdir(parents=True, exist_ok=True)

def download_data() -> bool:
    filename = ""
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
        return True
    except:
        return False

download_data()