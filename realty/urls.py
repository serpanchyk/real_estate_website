from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'apartments', views.ApartmentViewSet, basename='apartment')
router.register(r'settlements', views.SettlementViewSet, basename='settlement')
router.register(r'people', views.PersonViewSet, basename='person')
router.register(r'estates', views.EstateViewSet, basename='estate')
router.register(r'contracts', views.ContractViewSet, basename='contract')
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r'contacts', views.ContactViewSet, basename='contact')
router.register(r'emails', views.EmailViewSet, basename='email')
router.register(r'estate-employees', views.EstateEmployeeViewSet, basename='estateemployee')
router.register(r'estate-owners', views.EstateOwnerViewSet, basename='estateowner')
router.register(r'houses', views.HouseViewSet, basename='house')
router.register(r'offices', views.OfficeViewSet, basename='office')
router.register(r'person-roles', views.PersonRoleViewSet, basename='personrole')
router.register(r'phones', views.PhoneViewSet, basename='phone')
router.register(r'analytics', views.AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path(
        'reports/estates-by-settlement/',
        views.EstateCountBySettlementReportView.as_view(),
        name='report-estates-by-settlement'
    ),
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
    path('dashboard/v2/', views.analytics_dashboard_bokeh, name='analytics_dashboard_bokeh'),
    path('', include(router.urls)),
    path("contract_list", views.contract_list, name="contract_list"),
    path("contract_list/<int:contract_id>/", views.contract_detail, name="contract_detail"),
    path("contract_list/<int:contract_id>/delete/", views.delete_contract, name="delete_contract"),
    path('create-contract/', views.create_contract, name='create_contract'),
]