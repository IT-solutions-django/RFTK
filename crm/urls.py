"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from invoice.views import InvoiceDocumentCreateView, add_organization, add_counterparty, pdf, get_banks, \
    generate_invoice_excel, get_banks_counterparty
from user import views
from utd.views import UtdDocumentCreateView
from vat_invoice.views import VatInvoiceDocumentCreateView
from packing_list.views import PackingListDocumentCreateView
from commercial_offer.views import CommercialOfferDocumentCreateView
from outlay.views import OutlayDocumentCreateView
from ks_2.views import Ks2DocumentCreateView
from ks_3.views import Ks3DocumentCreateView
from act_service.views import ActServiceDocumentCreateView
from power_attorney.views import PowerAttorneyDocumentCreateView
from sales_receipt.views import SalesReceiptDocumentCreateView
from user.views import find_company_by_inn, find_bank_by_bik
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', InvoiceDocumentCreateView.as_view(), name='invoice'),
    path('utd/', UtdDocumentCreateView.as_view(), name='utd'),
    path('vat-invoice/', VatInvoiceDocumentCreateView.as_view(), name='vat-invoice'),
    path('packing-list/', PackingListDocumentCreateView.as_view(), name='packing-list'),
    path('commercial-offer/', CommercialOfferDocumentCreateView.as_view(), name='commercial-offer'),
    path('outlay/', OutlayDocumentCreateView.as_view(), name='outlay'),
    path('ks-2/', Ks2DocumentCreateView.as_view(), name='ks-2'),
    path('ks-3/', Ks3DocumentCreateView.as_view(), name='ks-3'),
    path('act-service/', ActServiceDocumentCreateView.as_view(), name='act-service'),
    path('power-attorney/', PowerAttorneyDocumentCreateView.as_view(), name='power-attorney'),
    path('sales-receipt/', SalesReceiptDocumentCreateView.as_view(), name='sales-receipt'),
    path('add-organization/', add_organization, name='add_organization'),
    path('add-counterparty/', add_counterparty, name='add_counterparty'),
    path('pdf/', pdf, name='pdf'),
    path('get_banks/', get_banks, name='get_banks'),
    path('get_banks_counterparty/', get_banks_counterparty, name='get_banks_counterparty'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('add-organization-profile/', views.add_organization_from_profile, name='add-organization-profile'),
    path('add-counterparty-profile/', views.add_counterparty_from_profile, name='add-counterparty-profile'),
    path('generate_invoice_excel/', generate_invoice_excel, name='generate_invoice_excel'),
    path('edit_organization/<int:id_org>', views.edit_organization, name='edit_organization'),
    path('edit_counterparty/<int:id_org>', views.edit_counterparty, name='edit_counterparty'),
    path('edit_document/<int:id_doc>', views.edit_document, name='edit_document'),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bik, name="find-bank"),
]
