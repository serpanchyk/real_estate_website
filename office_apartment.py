from apartment import Apartment
from office import Office

class ApartmentOffice(Apartment, Office):
    DEFAULT_RATE = 0.1

    def __init__(self, residential_complex_name, kitchen_area,
                 balcony, openspace, conference_rooms, security,
                 area, rooms, floor, total_floors, elevator, parking,
                 estate_id, settlement, street, house_number,
                 apartment_number, year_built, transaction_type,
                 price, status):
        kwargs = {
            'estate_id': estate_id, 'settlement': settlement, 'street': street,
            'house_number': house_number, 'apartment_number': apartment_number,
            'year_built': year_built, 'transaction_type': transaction_type,
            'price': price, 'status': status,
            'residential_complex_name': residential_complex_name, 'kitchen_area': kitchen_area,
            'balcony': balcony, 'rooms': rooms,
            'openspace': openspace, 'conference_rooms': conference_rooms, 'security': security,
            'area': area, 'floor': floor, 'total_floors': total_floors,
            'elevator': elevator, 'parking': parking
        }

        super().__init__(**kwargs)

    def get_address(self):
        return f"Live/Work: {self.house_number}, {self.street} ST, APT: {self.apartment_number}, {self.settlement.get_settlement_full_info()}"

    def calculate_commission(self):
        return self._price * self.DEFAULT_RATE
