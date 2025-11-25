from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from django.db.models import Count, Sum, Avg, Q, Max
from django.db.models.functions import TruncMonth

from .models import (
    Apartment, AuthGroup, AuthUser, Contact, Contract, Email, Estate, EstateEmployee,
    EstateOwner, House, Office, Person, PersonRole, Phone, Role, Settlement,
)
from django.db import models

T = TypeVar('T', bound=models.Model)


class AbstractRepository(ABC, Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, obj_id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, **kwargs) -> T:
        raise NotImplementedError

    @abstractmethod
    def update(self, obj_id: int, **kwargs) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, obj_id: int) -> None:
        raise NotImplementedError


class DjangoORMRepository(AbstractRepository[T]):
    def get_all(self) -> List[T]:
        return list(self.model.objects.all())

    def get_by_id(self, obj_id: int) -> T | None:
        try:
            return self.model.objects.get(pk=obj_id)
        except self.model.DoesNotExist:
            return None

    def create(self, **kwargs) -> T:
        obj = self.model.objects.create(**kwargs)
        return obj

    def update(self, obj_id: int, **kwargs) -> T | None:
        obj = self.get_by_id(obj_id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            obj.save()
            return obj
        return None

    def delete(self, obj_id: int) -> None:
        obj = self.get_by_id(obj_id)
        if obj:
            obj.delete()


class ApartmentRepository(DjangoORMRepository[Apartment]):
    def __init__(self):
        super().__init__(Apartment)

    def stats_by_rooms(self):
        return self.model.objects.values('rooms').annotate(
            avg_price=Avg('estate__price'),
            max_price=Max('estate__price'),
            supply_count=Count('estate_id')
        ).order_by('rooms')


class AuthGroupRepository(DjangoORMRepository[AuthGroup]):
    def __init__(self):
        super().__init__(AuthGroup)


class AuthUserRepository(DjangoORMRepository[AuthUser]):
    def __init__(self):
        super().__init__(AuthUser)

    def create(self, **kwargs) -> AuthUser:
        return self.model.objects.create_user(**kwargs)


class ContactRepository(DjangoORMRepository[Contact]):
    def __init__(self):
        super().__init__(Contact)


class ContractRepository(DjangoORMRepository[Contract]):
    def __init__(self):
        super().__init__(Contract)

    def monthly_revenue_stream(self):
        return self.model.objects.annotate(
            month=TruncMonth('date_signed')
        ).values('month').annotate(
            total_revenue=Sum('payment_amount'),
            total_deals=Count('contract_id')
        ).order_by('month')


class EmailRepository(DjangoORMRepository[Email]):
    def __init__(self):
        super().__init__(Email)


class EstateRepository(DjangoORMRepository[Estate]):
    def __init__(self):
        super().__init__(Estate)

    def get_price_matrix(self):
        return self.model.objects.values(
            'settlement__name',
            'transaction_type'
        ).annotate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            inventory_count=Count('estate_id')
        ).order_by('settlement__name')


class EstateEmployeeRepository(DjangoORMRepository[EstateEmployee]):
    def __init__(self):
        super().__init__(EstateEmployee)


class EstateOwnerRepository(DjangoORMRepository[EstateOwner]):
    def __init__(self):
        super().__init__(EstateOwner)


class HouseRepository(DjangoORMRepository[House]):
    def __init__(self):
        super().__init__(House)


class OfficeRepository(DjangoORMRepository[Office]):
    def __init__(self):
        super().__init__(Office)


class PersonRepository(DjangoORMRepository[Person]):
    def __init__(self):
        super().__init__(Person)

    def top_revenue_employees(self):
        return self.model.objects.filter(
            contract__isnull=False
        ).annotate(
            total_sales_volume=Sum('contract__payment_amount'),
            deals_closed=Count('contract')
        ).order_by('-total_sales_volume').values("surname", "total_sales_volume")

    def top_owners(self, threshold=0):
        return (self.model.objects
                .annotate(total_assets=Sum("owned_estates__price"))
                .filter(total_assets__gte=threshold)
                .order_by("-total_assets")
                .values("name", "surname", "total_assets"))


class PersonRoleRepository(DjangoORMRepository[PersonRole]):
    def __init__(self):
        super().__init__(PersonRole)


class PhoneRepository(DjangoORMRepository[Phone]):
    def __init__(self):
        super().__init__(Phone)


class RoleRepository(DjangoORMRepository[Role]):
    def __init__(self):
        super().__init__(Role)


class SettlementRepository(DjangoORMRepository[Settlement]):
    def __init__(self):
        super().__init__(Settlement)

    def hot_settlements(self, threshold=1):
        output = (Settlement.objects.annotate(
            number_of_estates=Count("estate"))
                  .filter(number_of_estates__gte=threshold)
                  .order_by("-number_of_estates")
                  .values("name", "number_of_estates"))

        return output


    def market_analysis(self):
        return self.model.objects.annotate(
            avg_house_price=Avg(
                'estate__price',
                filter=Q(estate__house__isnull=False)
            ),
            avg_apartment_price=Avg(
                'estate__price',
                filter=Q(estate__apartment__isnull=False)
            )
        ).values('name', 'avg_house_price', 'avg_apartment_price')


class UnitOfWork:
    def __init__(self):
        self.apartments = ApartmentRepository()
        self.auth_groups = AuthGroupRepository()
        self.auth_users = AuthUserRepository()
        self.contacts = ContactRepository()
        self.contracts = ContractRepository()
        self.emails = EmailRepository()
        self.estates = EstateRepository()
        self.estate_employees = EstateEmployeeRepository()
        self.estate_owners = EstateOwnerRepository()
        self.houses = HouseRepository()
        self.offices = OfficeRepository()
        self.people = PersonRepository()
        self.person_roles = PersonRoleRepository()
        self.phones = PhoneRepository()
        self.roles = RoleRepository()
        self.settlements = SettlementRepository()