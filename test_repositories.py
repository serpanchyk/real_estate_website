import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_project.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error installing django: {e}")
    exit()

from realty.repositories import UnitOfWork

def run_demonstration():
    uow = UnitOfWork()

    print('GET ALL:')
    all_persons = uow.people.get_all()
    print(f"Found {len(all_persons)} people.")
    if all_persons:
        first_person = all_persons[0]
        print(f"First person: {first_person.name} {first_person.surname}")

    print('GET BY ID:')
    estate_id_to_find = 300
    found_estate = uow.estates.get_by_id(estate_id_to_find)
    if found_estate:
        print(f"Found estate with ID {estate_id_to_find}: {found_estate}")
    else:
        print(f"No estate found with ID {estate_id_to_find}")

    test_estate = uow.estates.get_by_id(300)
    test_employee = uow.people.get_by_id(260)
    test_client = uow.people.get_by_id(872)

    new_contract_data = {
        'contract_id' : 1000,
        'estate' : test_estate,
        'employee' : test_employee,
        'client' : test_client,
        'contract_type' : 'продаж',
        'date_signed' : '2024-10-01',
        'start_date' : '2024-10-01',
        'end_date' : '2025-10-01',
        'payment_amount' : 250000.00,
        'fee_percentage' : 3.5,
        'terms' : 'Standard sale contract terms apply.'
    }

    created_contract = uow.contracts.create(**new_contract_data)
    print(f"Created contract with ID {created_contract.pk}: {created_contract}")
    input("Press enter to continue...")

    updated_contract = uow.contracts.update(created_contract.pk, terms='Updated Terms')
    print(f"Updated contract with ID {updated_contract.pk}: {updated_contract}")
    input("Press enter to continue...")

    uow.contracts.delete(created_contract.pk)
    print(f"Deleted contract with ID {created_contract.pk}")

run_demonstration()