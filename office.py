from estate import Estate

class Office(Estate):
    DEFAULT_RATE = 0.05

    def __init__(self, area=None, floor=None, total_floors=None, openspace=None, conference_rooms=None,
                 parking=None, elevator=None, security=None, **kwargs):
        self.area = area
        self.floor = floor
        self.total_floors = total_floors
        self.openspace = openspace
        self.conference_rooms = conference_rooms
        self.parking = parking
        self.elevator = elevator
        self.security = security

        super().__init__(**kwargs)

    def get_address(self):
        return f"{self.house_number}, {self.street} ST, APT: {self.apartment_number}, {self.settlement.get_settlement_full_info()}"

    def calculate_commission(self):
        return self._price * self.DEFAULT_RATE

