from abc import ABC, abstractmethod


class Estate(ABC):
    def __init__(self, estate_id, settlement,
                 street, house_number, apartment_number,
                 year_built, transaction_type, price,
                 status, **kwargs):

        self.estate_id = estate_id
        self.settlement = settlement
        self.street = street
        self.house_number = house_number
        self.apartment_number = apartment_number
        self.year_built = year_built
        self.transaction_type = transaction_type
        self._price = price
        self.status = status

        super().__init__(**kwargs)

    @abstractmethod
    def calculate_commission(self):
        pass

    @abstractmethod
    def get_address(self):
        pass

    @property
    def price(self):
        return f"{self._price:.2f} ₴"

    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, (int, float)):
            raise TypeError("price is not a number")
        elif new_price <= 0:
            raise ValueError("price must be greater than 0")

        self._price = new_price


class Settlement:
    VALID_TYPES = ["Місто", "Селище міського типу", "Село", "Районний центр", "Обласний центр"]

    def __init__(self, settlement_id, name,
                 amalgamated_hromada, oblast, type):
        if not Settlement.is_valid_settlement_type(type):
            raise ValueError(f"Invalid settlement type: '{type}'. Must be one of {Settlement.VALID_TYPES}")

        self.settlement_id = settlement_id
        self.name = name
        self.amalgamated_hromada = amalgamated_hromada
        self.oblast = oblast
        self.type = type

    @staticmethod
    def is_valid_settlement_type(settlement_type):
        return settlement_type in Settlement.VALID_TYPES

    def get_settlement_full_info(self):
        return f"{self.type} {self.name}, {self.amalgamated_hromada}, {self.oblast}"