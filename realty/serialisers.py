from .models import (
    Apartment, Contact, Contract, Email, Estate,
    EstateEmployee, EstateOwner, House, Office, Person, PersonRole,
    Phone, Role, Settlement
)
from rest_framework import serializers

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'

class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = '__all__'

class EstateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateEmployee
        fields = '__all__'

class EstateOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstateOwner
        fields = '__all__'

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class PersonRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRole
        fields = '__all__'

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = '__all__'


