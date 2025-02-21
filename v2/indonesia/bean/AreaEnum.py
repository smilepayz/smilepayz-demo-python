
from enum import Enum, auto

class CurrencyEnum(Enum):
    IDR = auto()
    THB = auto()
    INR = auto()
    BRL = auto()
    MXN = auto()

class AreaEnum(Enum):

    INDONESIA = (10, CurrencyEnum.IDR, 62)
    THAILAND = (11, CurrencyEnum.THB, 66)
    INDIA = (12, CurrencyEnum.INR, 91)
    BRAZIL = (13, CurrencyEnum.BRL, 55)
    MEXICO = (14, CurrencyEnum.MXN, 52)

    def __init__(self, code, currency, country_id):
        self._code = code
        self._currency = currency
        self._country_id = country_id

    @property
    def code(self):
        return self._code

    @property
    def currency(self):
        return self._currency

    @property
    def country_id(self):
        return self._country_id

    @classmethod
    def from_code(cls, code):
        for area in cls:
            if area.code == code:
                return area
        raise ValueError(f"No matching AreaEnum for code: {code}")