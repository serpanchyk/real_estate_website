from estate import Estate

class Apartment(Estate):
    DEFAULT_RATE = 0.08

    def __init__(self, residential_complex_name=None, area=None, kitchen_area=None, rooms=None,
                 floor=None, total_floors=None, elevator=None, balcony=None, **kwargs):
        self.residential_complex_name = residential_complex_name
        self.area = area
        self.kitchen_area = kitchen_area
        self.rooms = rooms
        self.floor = floor
        self.total_floors = total_floors
        self.elevator = elevator
        self.balcony = balcony

        super().__init__(**kwargs)

    def get_address(self):
        return f"{self.house_number}, {self.street} ST, APT: {self.apartment_number}, {self.settlement.get_settlement_full_info()}"

    def calculate_commission(self):
        return self._price * self.DEFAULT_RATE