import os
from pathlib import Path


path = Path(__file__).parent
Path(path / "zipdir").mkdir(parents=True, exist_ok=True)
Path(path / 'datadir').mkdir(parents=True, exist_ok=True)

def cleaner(ending):
    path = Path(__file__).resolve().parents[1] / 'zipdir'
    for f in os.listdir(path):
        if ending in f:
            os.remove(os.path.join(path, f))

cleaner('dat')