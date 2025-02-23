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
    generate_invoice_excel, get_banks_counterparty, add_organization_with_bank, add_counterparty_with_bank, \
    invoice_document
from user import views
from utd.views import UtdDocumentCreateView, utd_document
from vat_invoice.views import VatInvoiceDocumentCreateView, vat_invoice_document
from packing_list.views import PackingListDocumentCreateView
from commercial_offer.views import CommercialOfferDocumentCreateView, commercial_offer_document
from outlay.views import OutlayDocumentCreateView, outlay_document
from ks_2.views import Ks2DocumentCreateView, ks_2_document
from ks_3.views import Ks3DocumentCreateView, ks_3_document
from act_service.views import ActServiceDocumentCreateView, act_service_document
from power_attorney.views import PowerAttorneyDocumentCreateView, power_attorney_document
from sales_receipt.views import SalesReceiptDocumentCreateView, sales_receipt_document
from pko.views import PkoDocumentCreateView, pko_document
from rko.views import RkoDocumentCreateView, rko_document
from user.views import find_company_by_inn, find_bank_by_bik, inn_autocomplete, bank_autocomplete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', InvoiceDocumentCreateView.as_view(), name='invoice'),
    path('invoice_document/', invoice_document, name='invoice_document'),
    path('utd/', UtdDocumentCreateView.as_view(), name='utd'),
    path('utd_document/', utd_document, name='utd_document'),
    path('vat-invoice/', VatInvoiceDocumentCreateView.as_view(), name='vat-invoice'),
    path('vat_invoice_document/', vat_invoice_document, name='vat_invoice_document'),
    path('packing-list/', PackingListDocumentCreateView.as_view(), name='packing-list'),
    path('commercial-offer/', CommercialOfferDocumentCreateView.as_view(), name='commercial-offer'),
    path('commercial_offer_document/', commercial_offer_document, name='commercial_offer_document'),
    path('outlay/', OutlayDocumentCreateView.as_view(), name='outlay'),
    path('outlay_document/', outlay_document, name='outlay_document'),
    path('ks-2/', Ks2DocumentCreateView.as_view(), name='ks-2'),
    path('ks_2_document/', ks_2_document, name='ks_2_document'),
    path('ks-3/', Ks3DocumentCreateView.as_view(), name='ks-3'),
    path('ks_3_document/', ks_3_document, name='ks_3_document'),
    path('act-service/', ActServiceDocumentCreateView.as_view(), name='act-service'),
    path('act_service_document/', act_service_document, name='act_service_document'),
    path('power-attorney/', PowerAttorneyDocumentCreateView.as_view(), name='power-attorney'),
    path('power_attorney_document/', power_attorney_document, name='power_attorney_document'),
    path('sales-receipt/', SalesReceiptDocumentCreateView.as_view(), name='sales-receipt'),
    path('sales_receipt_document/', sales_receipt_document, name='sales_receipt_document'),
    path('pko/', PkoDocumentCreateView.as_view(), name='pko'),
    path('pko_document/', pko_document, name='pko_document'),
    path('rko/', RkoDocumentCreateView.as_view(), name='rko'),
    path('rko_document/', rko_document, name='rko_document'),
    path('add-organization/', add_organization, name='add_organization'),
    path('add_organization_with_bank/', add_organization_with_bank, name='add_organization_with_bank'),
    path('add-counterparty/', add_counterparty, name='add_counterparty'),
    path('add_counterparty_with_bank/', add_counterparty_with_bank, name='add_counterparty_with_bank'),
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
    path('edit_document/<int:id_doc>/<str:doc_type>/', views.edit_document, name='edit_document'),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bik, name="find-bank"),
    path('inn_autocomplete/', inn_autocomplete, name='inn_autocomplete'),
    path('bank_autocomplete/', bank_autocomplete, name='bank_autocomplete'),
    path('document/<str:doc_type>/<int:document_id>/print/', views.print_document, name='print_document'),
]
