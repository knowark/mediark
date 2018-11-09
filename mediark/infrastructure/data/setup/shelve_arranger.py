import shelve
from pathlib import Path


class ShelveArranger:

    @staticmethod
    def make_shelve(filename: str) -> None:
        parent_path = Path(filename).parent
        parent_path.mkdir(parents=True, exist_ok=True)
        with shelve.open(filename, 'c'):
            pass
