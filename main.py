from estate import Settlement
from house import House
from office_apartment import Office, Apartment, ApartmentOffice


def main():
    lviv = Settlement(10, "Львів", "Львівська ОТГ", "Львівська область", "Обласний центр")
    print("--- Демонстрація Класів Нерухомості у Львові ---")
    print(f"Інформація про населений пункт: {lviv.get_settlement_full_info()}")
    print("-" * 40)

    valid_check = Settlement.is_valid_settlement_type('Місто')
    invalid_check = Settlement.is_valid_settlement_type('Станиця')
    print(f"Перевірка типу 'Місто': {valid_check}")
    print(f"Перевірка типу 'Станиця': {invalid_check}")
    print("-" * 40)

    apt_lviv = Apartment(residential_complex_name="Avalon Comfort", area=85.5, kitchen_area=18, rooms=3, floor=7,
                         total_floors=16, elevator=True, balcony=True,
                         estate_id=1001, settlement=lviv, street="Проспект Червоної Калини", house_number=90,
                         apartment_number=42, year_built=2022, transaction_type="Продаж", price=120000, status="Вільна")

    house_lviv = House(land_area=600, floors=3, rooms=6, garage=True, parking=True, basement=True, garden=True,
                       heating_type="Газове",
                       estate_id=2002, settlement=lviv, street="Івасюка", house_number=5, apartment_number=None,
                       year_built=2008, transaction_type="Продаж", price=350000, status="Вільна")

    office_lviv = Office(area=300, floor=2, total_floors=5, openspace=True, conference_rooms=4, parking=True,
                         elevator=True, security=True,
                         estate_id=3003, settlement=lviv, street="Шевченка", house_number=10, apartment_number=None,
                         year_built=2015, transaction_type="Оренда", price=80000, status="Зайнятий")

    mixed_lviv = ApartmentOffice(residential_complex_name="Art House", kitchen_area=12, balcony=False, openspace=False,
                                 conference_rooms=1, security=False,
                                 area=140, rooms=4, floor=3, total_floors=4, elevator=False, parking=True,
                                 estate_id=4004, settlement=lviv, street="Площа Ринок", house_number=3,
                                 apartment_number=10, year_built=1905, transaction_type="Продаж", price=400000,
                                 status="Вільна")

    properties = [apt_lviv, house_lviv, office_lviv, mixed_lviv]

    for p in properties:
        print(f"Тип: {p.__class__.__name__}")
        print(f"Адреса: {p.get_address()}")
        print(f"Ціна: {p.price}")
        print(f"Ставка комісії: {p.DEFAULT_RATE * 100:.1f}%")
        print(f"Сума комісії: {p.calculate_commission():.2f} ₴")
        print("-" * 40)

if __name__ == '__main__':
    main()