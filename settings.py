import pathlib
from typing import Final

ROOT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parent

DB_PATH: Final[pathlib.Path] = ROOT_PATH.joinpath('db', 'db.sqlite')

DB_PHONES_PATH: Final[pathlib.Path] = ROOT_PATH.joinpath('db', 'db_phones.sqlite')
