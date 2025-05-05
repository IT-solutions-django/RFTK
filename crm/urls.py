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
    invoice_document, main, add_bank_org, add_bank_coun, invoice_registry
from user import views
from utd.views import UtdDocumentCreateView, utd_document, utd_registry
from vat_invoice.views import VatInvoiceDocumentCreateView, vat_invoice_document, vat_invoice_registry
from packing_list.views import PackingListDocumentCreateView
from commercial_offer.views import CommercialOfferDocumentCreateView, commercial_offer_document, commercial_offer_registry
from outlay.views import OutlayDocumentCreateView, outlay_document, outlay_registry
from ks_2.views import Ks2DocumentCreateView, ks_2_document, ks_2_registry
from ks_3.views import Ks3DocumentCreateView, ks_3_document, ks_3_registry
from act_service.views import ActServiceDocumentCreateView, act_service_document, act_services_registry
from power_attorney.views import PowerAttorneyDocumentCreateView, power_attorney_document, power_attorney_registry
from sales_receipt.views import SalesReceiptDocumentCreateView, sales_receipt_document, sales_receipt_registry
from pko.views import PkoDocumentCreateView, pko_document, pko_registry
from rko.views import RkoDocumentCreateView, rko_document, rko_registry
from reconciliation.views import ReconciliationCreateView, reconciliation_document, reconciliation_registry
from agreement.views import AgreementDocumentCreateView, agreement_document, agreement_registry
from user.views import find_company_by_inn, find_bank_by_bik, inn_autocomplete, bank_autocomplete, add_template_document, get_labels, get_value_labels, add_labels, copy_document, download_document, create_other_document
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('invoice/', InvoiceDocumentCreateView.as_view(), name='invoice'),
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
    path('reconciliation/', ReconciliationCreateView.as_view(), name='reconciliation'),
    path('reconciliation_document/', reconciliation_document, name='reconciliation_document'),
    path('agreement/', AgreementDocumentCreateView.as_view(), name='agreement'),
    path('agreement_document/', agreement_document, name='agreement_document'),
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
    path('copy_document/<int:id_doc>/<str:doc_type>/', copy_document, name='copy_document'),
    path("find-company/", find_company_by_inn, name="find-company"),
    path("find-bank/", find_bank_by_bik, name="find-bank"),
    path('inn_autocomplete/', inn_autocomplete, name='inn_autocomplete'),
    path('bank_autocomplete/', bank_autocomplete, name='bank_autocomplete'),
    path('document/<str:doc_type>/<int:document_id>/print/', views.print_document, name='print_document'),
    path('document/<str:doc_type>/<int:document_id>/download/', download_document, name='download_document'),
    path('add_template_document/', add_template_document, name='add-template-document'),
    path('get_labels/', get_labels, name='get-labels'),
    path('get_saved_values/', get_value_labels, name='get-value-labels'),
    path('add_labels/', add_labels, name='add_labels'),
    path('add_bank_org/', add_bank_org, name='add_bank_org'),
    path('add_bank_coun/', add_bank_coun, name='add_bank_coun'),
    path('api/search-counterparty/', views.search_counterparty, name='search_counterparty'),
    path('create_other_document/<int:id_doc>/', create_other_document, name='create_other_document'),
    path('utd_registry/', utd_registry, name='utd_registry'),
    path('invoice_registry/', invoice_registry, name='invoice_registry'),
    path('vat_invoice_registry/', vat_invoice_registry, name='vat_invoice_registry'),
    path('commercial_offer_registry/', commercial_offer_registry, name='commercial_offer_registry'),
    path('outlay_registry/', outlay_registry, name='outlay_registry'),
    path('ks_2_registry/', ks_2_registry, name='ks_2_registry'),
    path('ks_3_registry/', ks_3_registry, name='ks_3_registry'),
    path('act_services_registry/', act_services_registry, name='act_services_registry'),
    path('power_attorney_registry/', power_attorney_registry, name='power_attorney_registry'),
    path('sales_receipt_registry/', sales_receipt_registry, name='sales_receipt_registry'),
    path('pko_registry/', pko_registry, name='pko_registry'),
    path('rko_registry/', rko_registry, name='rko_registry'),
    path('reconciliation_registry/', reconciliation_registry, name='reconciliation_registry'),
    path('agreement_registry/', agreement_registry, name='agreement_registry'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
