import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from . import models as m
from .forms import ContractForm
from .repositories import UnitOfWork
from . import serialisers as s
from django.db.models import Count
from rest_framework.views import APIView
from math import pi
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Spectral6, Magma256, Viridis256
from bokeh.transform import cumsum, factor_cmap
from bokeh.resources import CDN, INLINE


def analytics_dashboard_bokeh(request):
    uow = UnitOfWork()

    try:
        top_cities_filter = int(request.GET.get('top_cities', 20))
        min_rooms_filter = int(request.GET.get('min_rooms', 0))
    except ValueError:
        top_cities_filter = 20
        min_rooms_filter = 0

    def safe_dataframe(data, float_cols=None, str_cols=None):
        df = pd.DataFrame(list(data))

        if df.empty:
            all_cols = (float_cols or []) + (str_cols or [])
            return pd.DataFrame({c: [] for c in all_cols})

        if float_cols:
            for col in float_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).astype(float)

        if str_cols:
            for col in str_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).fillna("")

        from decimal import Decimal
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].apply(lambda x: float(x) if isinstance(x, Decimal) else x)

        return df

    df_rev = safe_dataframe(
        uow.contracts.monthly_revenue_stream(),
        float_cols=['total_revenue']
    )

    if not df_rev.empty and 'month' in df_rev.columns:
        df_rev['month'] = pd.to_datetime(df_rev['month'])

    df_hot = safe_dataframe(
        uow.settlements.hot_settlements(),
        float_cols=['number_of_estates'],
        str_cols=['name']
    )

    if not df_hot.empty:
        df_hot = df_hot.groupby('name', as_index=False)['number_of_estates'].sum()

    df_hot = df_hot.sort_values('number_of_estates', ascending=False).head(top_cities_filter)

    df_mkt = safe_dataframe(
        uow.settlements.market_analysis(),
        float_cols=['avg_house_price', 'avg_apartment_price'],
        str_cols=['name']
    )

    if not df_mkt.empty:
        df_mkt = df_mkt.groupby('name', as_index=False)[['avg_house_price', 'avg_apartment_price']].mean()

    df_rooms = safe_dataframe(
        uow.apartments.stats_by_rooms(),
        float_cols=['avg_price', 'rooms']
    )

    if not df_rooms.empty:
        df_rooms = df_rooms[df_rooms['rooms'] >= min_rooms_filter]

    df_emp = safe_dataframe(
        uow.people.top_revenue_employees(),
        float_cols=['total_sales_volume'],
        str_cols=['surname']
    )

    df_whale = safe_dataframe(
        uow.people.top_owners(),
        float_cols=['total_assets'],
        str_cols=['surname']
    ).sort_values('total_assets', ascending=False).head(5)

    source_rev = ColumnDataSource(df_rev)
    p1 = figure(title="Monthly Revenue Trend", x_axis_type="datetime", height=350, sizing_mode="stretch_width")
    if not df_rev.empty:
        p1.line(x='month', y='total_revenue', source=source_rev, line_width=3, color="green", legend_label="Revenue")
        p1.scatter(x='month', y='total_revenue', source=source_rev, size=8, color="green")
        p1.add_tools(HoverTool(tooltips=[("Date", "@month{%F}"), ("Revenue", "$@total_revenue{0.00 a}")],
                               formatters={'@month': 'datetime'}))

    source_hot = ColumnDataSource(df_hot)
    cities = df_hot['name'].tolist()
    p2 = figure(x_range=cities, title=f"Most Active Markets (Top {top_cities_filter})", height=350,
                sizing_mode="stretch_width")
    if not df_hot.empty:
        palette = Magma256[:len(cities)] if len(cities) <= 256 else Magma256
        p2.vbar(x='name', top='number_of_estates', width=0.8, source=source_hot,
                line_color='white', fill_color=factor_cmap('name', palette=palette, factors=cities))
    p2.xaxis.major_label_orientation = 1.2

    source_rooms = ColumnDataSource(df_rooms)
    p3 = figure(title="Price vs Rooms Correlation", height=350, sizing_mode="stretch_width")
    if not df_rooms.empty:
        p3.scatter(x='rooms', y='avg_price', size=15, source=source_rooms, color="navy", alpha=0.6)
        p3.add_tools(HoverTool(tooltips=[("Rooms", "@rooms"), ("Avg Price", "$@avg_price{0.00 a}")]))
    p3.xaxis.axis_label = "Number of Rooms"
    p3.yaxis.axis_label = "Average Price"

    df_emp_sorted = df_emp.sort_values('total_sales_volume', ascending=True).tail(10)
    source_emp = ColumnDataSource(df_emp_sorted)
    employees = df_emp_sorted['surname'].tolist()
    p4 = figure(y_range=employees, title="Top Agents", height=350, sizing_mode="stretch_width")
    if not df_emp.empty:
        p4.hbar(y='surname', right='total_sales_volume', height=0.8, source=source_emp, color="#8B5CF6")
        p4.add_tools(HoverTool(tooltips=[("Agent", "@surname"), ("Sales", "$@total_sales_volume{0.00 a}")]))

    source_mkt = ColumnDataSource(df_mkt)
    mkt_cities = df_mkt['name'].tolist()
    p5 = figure(x_range=mkt_cities, title="House (Blue) vs Apt (Red) Prices", height=350, sizing_mode="stretch_width")
    if not df_mkt.empty:
        p5.vbar(x='name', top='avg_house_price', width=0.4, source=source_mkt, color="blue", legend_label="House")
        p5.scatter(x='name', y='avg_apartment_price', size=10, source=source_mkt, color="red", legend_label="Apartment")
        p5.add_tools(
            HoverTool(tooltips=[("City", "@name"), ("House", "$@avg_house_price"), ("Apt", "$@avg_apartment_price")]))
    p5.xaxis.major_label_orientation = 1.2

    if not df_whale.empty and df_whale['total_assets'].sum() > 0:
        df_whale['angle'] = df_whale['total_assets'] / df_whale['total_assets'].sum() * 2 * pi
        count = len(df_whale)
        if count <= 6:
            df_whale['color'] = Spectral6[:count]
        else:
            df_whale['color'] = Magma256[:count] if count <= 256 else Magma256[:256]
    else:
        df_whale['angle'] = []
        df_whale['color'] = []

    source_whale = ColumnDataSource(df_whale)
    p6 = figure(title="Top 20 Whale Owners", height=350, sizing_mode="stretch_width",
                tooltips="@surname: @total_assets{0.00 a}")
    if not df_whale.empty:
        p6.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                 line_color="white", fill_color='color', legend_field='surname', source=source_whale)
    p6.axis.axis_label = None
    p6.axis.visible = False
    p6.grid.grid_line_color = None

    script, divs = components({
        'revenue': p1, 'hot': p2, 'rooms': p3,
        'employees': p4, 'market': p5, 'whale': p6
    })

    resources = INLINE.render()

    return render(request, "dashboard_bokeh.html", {
        'script': script,
        'divs': divs,
        'resources': resources,
        'current_filters': {
            'top_cities': top_cities_filter,
            'min_rooms': min_rooms_filter
        }
    })


class AnalyticsViewSet(viewsets.ViewSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uow = UnitOfWork()

    def _queryset_to_response(self, queryset):
        if hasattr(queryset, 'values'):
            data_list = list(queryset.values())
        else:
            data_list = list(queryset)

        df = pd.DataFrame(data_list)

        if df.empty:
            return Response([])

        df.fillna(0)

        return Response(df.to_dict(orient='records'))

    @action(detail=False, methods=['get'], url_path='general-statistics')
    def get_general_statistics(self, request):
        revenue_data = self.uow.contracts.monthly_revenue_stream()

        df = pd.DataFrame(list(revenue_data))

        stats = {
            "description": "Monthly revenue statistics (based on signed contracts)",
            "data": None
        }

        if not df.empty:
            stats["data"] = {
                "mean": round(df['total_revenue'].mean(), 2),
                "median": round(df['total_revenue'].median(), 2),
                "max": round(df['total_revenue'].max(), 2),
                "min": round(df['total_revenue'].min(), 2)
            }

        return Response(stats)

    @action(detail=False, methods=['get'], url_path='settlements/hot')
    def hot_settlements(self, request):
        data = self.uow.settlements.hot_settlements()
        return self._queryset_to_response(data)

    @action(detail=False, methods=['get'], url_path='employees/top')
    def top_employees(self, request):
        data = self.uow.people.top_revenue_employees()
        return self._queryset_to_response(data)

    @action(detail=False, methods=['get'], url_path='owners/whales')
    def whale_owners(self, request):
        data = self.uow.people.top_owners()
        return self._queryset_to_response(data)

    @action(detail=False, methods=['get'], url_path='settlements/market')
    def market_analysis(self, request):
        data = self.uow.settlements.market_analysis()
        return self._queryset_to_response(data)

    @action(detail=False, methods=['get'], url_path='financials/monthly')
    def monthly_revenue(self, request):
        data = self.uow.contracts.monthly_revenue_stream()
        return self._queryset_to_response(data)

    @action(detail=False, methods=['get'], url_path='apartments/rooms')
    def stats_by_rooms(self, request):
        data = self.uow.apartments.stats_by_rooms()
        return self._queryset_to_response(data)


def analytics_dashboard(request):
    return render(request, "dashboard.html")


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
        item = self.repository.get_by_id(pk)
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
        item_to_delete = self.repository.get_by_id(pk)
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