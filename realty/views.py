from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from . import models as m
from .forms import ContractForm
from .repositories import UnitOfWork
from . import serialisers as s
from django.db.models import Count
from rest_framework.views import APIView

class BaseRepositoryViewSet(viewsets.ViewSet):

    serializer_class = None
    queryset = None
    repository_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uow = UnitOfWork()
        if self.repository_name:
            self.repository = getattr(self.uow, self.repository_name)
        else:
            raise AttributeError("ViewSet must define 'repository_name'.")

    def list(self, request):
        items = self.repository.get_all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        item = self.repository.get_by_id(pk)  # pk=pk - не обов'язково
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_item = self.repository.create(**serializer.validated_data)
            return Response(self.serializer_class(new_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        item_to_update = self.repository.get_by_id(pk)
        if item_to_update is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(item_to_update, data=request.data)
        if serializer.is_valid():
            updated_item = self.repository.update(pk, **serializer.validated_data)
            return Response(self.serializer_class(updated_item).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        item_to_delete = self.repository.get_by_id(pk)  # Використовуємо інше ім'я змінної
        if item_to_delete is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.repository.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

class EstateCountBySettlementReportView(APIView):
    def get(self, request, format=None):
        report_data = m.Settlement.objects.annotate(
            estate_count=Count('estate')
        ).values(
            'settlement_id',
            'name',
            'oblast',
            'estate_count'
        )

        return Response(list(report_data))

class ApartmentViewSet(BaseRepositoryViewSet):
    serializer_class = s.ApartmentSerializer
    queryset = m.Apartment.objects.all()
    repository_name = "apartments"


class SettlementViewSet(BaseRepositoryViewSet):
    serializer_class = s.SettlementSerializer
    queryset = m.Settlement.objects.all()
    repository_name = "settlements"


class PersonViewSet(BaseRepositoryViewSet):
    serializer_class = s.PersonSerializer
    queryset = m.Person.objects.all()
    repository_name = "people"


class EstateViewSet(BaseRepositoryViewSet):
    serializer_class = s.EstateSerializer
    queryset = m.Estate.objects.all()
    repository_name = "estates"


class ContractViewSet(BaseRepositoryViewSet):
    serializer_class = s.ContractSerializer
    queryset = m.Contract.objects.all()
    repository_name = "contracts"


class RoleViewSet(BaseRepositoryViewSet):
    serializer_class = s.RoleSerializer
    queryset = m.Role.objects.all()
    repository_name = "roles"


class ContactViewSet(BaseRepositoryViewSet):
    serializer_class = s.ContactSerializer
    queryset = m.Contact.objects.all()
    repository_name = "contacts"


class EmailViewSet(BaseRepositoryViewSet):
    serializer_class = s.EmailSerializer
    queryset = m.Email.objects.all()
    repository_name = "emails"


class EstateEmployeeViewSet(BaseRepositoryViewSet):
    serializer_class = s.EstateEmployeeSerializer
    queryset = m.EstateEmployee.objects.all()
    repository_name = "estate_employees"


class EstateOwnerViewSet(BaseRepositoryViewSet):
    serializer_class = s.EstateOwnerSerializer
    queryset = m.EstateOwner.objects.all()
    repository_name = "estate_owners"


class HouseViewSet(BaseRepositoryViewSet):
    serializer_class = s.HouseSerializer
    queryset = m.House.objects.all()
    repository_name = "houses"


class OfficeViewSet(BaseRepositoryViewSet):
    serializer_class = s.OfficeSerializer
    queryset = m.Office.objects.all()
    repository_name = "offices"


class PersonRoleViewSet(BaseRepositoryViewSet):
    serializer_class = s.PersonRoleSerializer
    queryset = m.PersonRole.objects.all()
    repository_name = "person_roles"


class PhoneViewSet(BaseRepositoryViewSet):
    serializer_class = s.PhoneSerializer
    queryset = m.Phone.objects.all()
    repository_name = "phones"


def contract_list(request):
    contract_list = m.Contract.objects.all()
    context = {"contract_list": contract_list}
    return render(request, "contract_list.html", context)

def contract_detail(request, contract_id):
    contract = get_object_or_404(m.Contract, pk=contract_id)
    return render(request, "contract_detail.html", {"contract": contract})

def create_contract(request):
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contract_list')
    else:
        form = ContractForm()

    return render(request, 'create_contract.html', {'form': form})

def delete_contract(request, contract_id):
    contract = get_object_or_404(m.Contract, pk=contract_id)

    if request.method == "POST":
        contract.delete()
        return redirect("contract_list")

    return redirect("contract_detail", contract_id=contract.contract_id)