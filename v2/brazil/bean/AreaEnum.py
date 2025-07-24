from enum import Enum, auto


class CurrencyEnum(Enum):
    BRL = auto()


class AreaEnum(Enum):
    BRAZIL = (CurrencyEnum.BRL, 55)

    def __init__(self, currency, country_id):
        # self._code = code
        self._currency = currency
        self._country_id = country_id

    # @property
    # def code(self):
    #     return self._code

    @property
    def currency(self):
        return self._currency

    @property
    def country_id(self):
        return self._country_id

    @classmethod
    def from_country_id(cls, country_id):
        for area in cls:
            if area.country_id == country_id:
                return area
        raise ValueError(f"No matching AreaEnum for country_id: {country_id}")
    #
    # @classmethod
    # def from_code(cls, code):
    #     for area in cls:
    #         if area.code == code:
    #             return area
    #     raise ValueError(f"No matching AreaEnum for code: {code}")
