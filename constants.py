import string
from typing import Final

PASSWORD_CHARACTERS: Final[str] = ''.join([
    string.ascii_letters,
    string.digits,
])

SPACE_API = 'http://api.open-notify.org/astros.json'

CHARACTERISTICS_URL = 'https://drive.google.com/uc?export=download&id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl'
