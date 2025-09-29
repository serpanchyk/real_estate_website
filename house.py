from estate import Estate

class House(Estate):
    DEFAULT_RATE = 0.03

    def __init__(self, land_area=None, floors=None, rooms=None, garage=None, parking=None,
                 basement=None, garden=None, heating_type=None, **kwargs):
        self.land_area = land_area
        self.floors = floors
        self.rooms = rooms
        self.garage = garage
        self.parking = parking
        self.basement = basement
        self.garden = garden
        self.heating_type = heating_type

        super().__init__(**kwargs)

    def get_address(self):
        return f"{self.house_number}, {self.street} ST, {self.settlement.get_settlement_full_info()}"

    def calculate_commission(self):
        return self._price * self.DEFAULT_RATE