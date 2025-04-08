from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TemplateDocumentForm
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm, \
    InvoiceDocumentForm, InvoiceDocumentTableFormSet
from invoice.models import InformationOrganization, Buyer, InvoiceDocument, BankDetailsOrganization, BankDetailsBuyer, \
    InvoiceDocumentTable, UtdDocument, VatInvoiceDocument, CommercialOfferDocument, OutlayDocument, Ks2Document, \
    Ks3Document, ActServiceDocument, PowerAttorneyDocument, SalesReceiptDocument, PkoDocument, RkoDocument, ReconciliationDocument, AgreementDocument, LabelTemplateDocument, TemplateDocument, ValueLabel
from utd.forms import UtdDocumentForm, UtdDocumentTableFormSet
from vat_invoice.forms import VatInvoiceDocumentForm
import requests
from django.http import JsonResponse
from utd.utils.excel import create_utd_excel
from invoice.utils.excel import create_invoice_excel
from vat_invoice.utils.excel import create_vat_invoice_excel
from commercial_offer.forms import CommercialOfferDocumentForm, CommercialOfferDocumentTableFormSet
from commercial_offer.utils.excel import create_commercial_offer_excel
from outlay.forms import OutlayDocumentForm
from outlay.utils.excel import create_outlay_excel
from ks_2.forms import Ks2DocumentForm, Ks2DocumentTableFormSet
from ks_2.utils.excel import create_ks2_excel
from ks_3.forms import Ks3DocumentForm, Ks3DocumentTableFormSet
from ks_3.utils.excel import create_ks3_excel
from act_service.forms import ActServiceDocumentForm
from act_service.utils.excel import create_act_service_excel
from power_attorney.forms import PowerAttorneyDocumentForm, PowerAttorneyDocumentTableFormSet
from power_attorney.utils.excel import create_power_attorney_excel
from sales_receipt.forms import SalesReceiptDocumentForm, SalesReceiptDocumentTableFormSet
from sales_receipt.utils.excel import create_sales_receipt_excel
from pko.forms import PkoDocumentForm
from pko.utils.excel import create_pko_excel
from rko.forms import RkoDocumentForm
from rko.utils.excel import create_rko_excel
from reconciliation.forms import ReconciliationDocumentForm, ReconciliationDocumentTableFormSet
from reconciliation.utils.excel import create_reconciliation_excel
from agreement.forms import AgreementDocumentForm
from agreement.utils.excel import create_agreement_excel


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')


@login_required
def profile(request):
    documents_by_category = {}

    all_documents = []
    for doc in InvoiceDocument.objects.all():
        all_documents.append({'type': 'Счет', 'instance': doc})

    for doc in UtdDocument.objects.all():
        all_documents.append({'type': 'УПД', 'instance': doc})

    for doc in VatInvoiceDocument.objects.all():
        all_documents.append({'type': 'Счет-фактура', 'instance': doc})

    for doc in all_documents:
        documents_by_category.setdefault(doc['type'], []).append(doc['instance'])

    counterparties = Buyer.objects.filter(user=request.user)
    organizations = InformationOrganization.objects.filter(user=request.user)
    return render(request, 'profile_new.html',
                  {
                      'organizations': organizations,
                      'counterparties': counterparties,
                      'documents_by_category': documents_by_category
                  }
                  )


def add_organization_from_profile(request):
    if request.method == 'POST':
        org_form = OrganizationForm(request.POST, request.FILES, prefix='organization')
        bank_form = BankDetailsOrganizationForm(request.POST, prefix='bank')

        if org_form.is_valid():
            organization = org_form.save(commit=False)
            organization.user = request.user
            organization.save()

            if any(bank_form.data.get('bank-' + field) for field in bank_form.fields):
                for field in bank_form.fields.values():
                    field.required = True
                if bank_form.is_valid():
                    bank_details = bank_form.save(commit=False)
                    bank_details.organization = organization
                    bank_details.save()
                else:
                    return render(request, 'add_organization_new.html', {
                        'org_form': org_form,
                        'bank_form': bank_form
                    })

            return redirect('profile')

    else:
        org_form = OrganizationForm(prefix='organization')
        bank_form = BankDetailsOrganizationForm(prefix='bank')

    return render(request, 'add_organization_new.html', {
        'org_form': org_form,
        'bank_form': bank_form
    })


def add_counterparty_from_profile(request):
    if request.method == 'POST':
        counterparty_form = CounterpartyForm(request.POST, prefix='counterparty')
        counterparty_bank_form = BankCounterpartyForm(request.POST, prefix='counterparty_bank')

        if counterparty_form.is_valid():
            organization = counterparty_form.save(commit=False)
            organization.user = request.user
            # organization.save()

            if any(counterparty_bank_form.data.get('counterparty_bank-' + field) for field in
                   counterparty_bank_form.fields):
                for field in counterparty_bank_form.fields.values():
                    field.required = True
                if counterparty_bank_form.is_valid():
                    organization.save()
                    bank_details = counterparty_bank_form.save(commit=False)
                    bank_details.organization = organization
                    bank_details.save()
                else:
                    return render(request, 'add_counterparty_new.html', {
                        'counterparty_form': counterparty_form,
                        'counterparty_bank_form': counterparty_bank_form
                    })

            organization.save()
            return redirect('profile')
    else:
        counterparty_form = CounterpartyForm(prefix='counterparty')
        counterparty_bank_form = BankCounterpartyForm(prefix='counterparty_bank')

    return render(request, 'add_counterparty_new.html',
                  {'counterparty_form': counterparty_form,
                   'counterparty_bank_form': counterparty_bank_form})


@login_required
def edit_organization(request, id_org):
    organization = InformationOrganization.objects.get(id=id_org)
    bank_details = BankDetailsOrganization.objects.filter(organization=organization).first()

    if request.method == 'POST':
        org_form = OrganizationForm(request.POST, request.FILES, instance=organization, prefix='organization')
        bank_form = BankDetailsOrganizationForm(request.POST, instance=bank_details, prefix='bank')

        if org_form.is_valid():
            organization = org_form.save(commit=False)
            organization.user = request.user
            organization.save()

            if any(bank_form.data.get('bank-' + field) for field in bank_form.fields):
                for field in bank_form.fields.values():
                    field.required = True
                if bank_form.is_valid():
                    bank_details_edit = bank_form.save(commit=False)
                    bank_details_edit.organization = organization
                    bank_details_edit.save()
                else:
                    return render(request, 'add_organization_new.html', {
                        'org_form': org_form,
                        'bank_form': bank_form
                    })

            return redirect('profile')

    else:
        org_form = OrganizationForm(instance=organization, prefix='organization')
        bank_form = BankDetailsOrganizationForm(instance=bank_details, prefix='bank')

    return render(request, 'add_organization_new.html', {
        'org_form': org_form,
        'bank_form': bank_form,
    })


@login_required
def edit_counterparty(request, id_org):
    counterparty = Buyer.objects.get(id=id_org)
    bank_details_counterparty = BankDetailsBuyer.objects.filter(organization=counterparty).first()

    if request.method == 'POST':
        counterparty_form = CounterpartyForm(request.POST, instance=counterparty, prefix='counterparty')
        counterparty_bank_form = BankCounterpartyForm(request.POST, instance=bank_details_counterparty,
                                                      prefix='counterparty_bank')

        if counterparty_form.is_valid():
            organization = counterparty_form.save(commit=False)
            organization.user = request.user
            organization.save()

            if any(counterparty_bank_form.data.get('counterparty_bank-' + field) for field in
                   counterparty_bank_form.fields):
                for field in counterparty_bank_form.fields.values():
                    field.required = True
                if counterparty_bank_form.is_valid():
                    bank_details_edit = counterparty_bank_form.save(commit=False)
                    bank_details_edit.organization = organization
                    bank_details_edit.save()
                else:
                    return render(request, 'add_counterparty_new.html', {
                        'counterparty_form': counterparty_form,
                        'counterparty_bank_form': counterparty_bank_form
                    })

            return redirect('profile')

    else:
        counterparty_form = CounterpartyForm(instance=counterparty, prefix='counterparty')
        counterparty_bank_form = BankCounterpartyForm(instance=bank_details_counterparty, prefix='counterparty_bank')

    return render(request, 'add_counterparty_new.html', {
        'counterparty_form': counterparty_form,
        'counterparty_bank_form': counterparty_bank_form,
    })


@login_required
def edit_document(request, id_doc, doc_type):
    document_model = None
    form_class = None
    formset_class = None
    template_name = ""

    document_mapping = {
        'invoice': {
            'model': InvoiceDocument,
            'form': InvoiceDocumentForm,
            'formset': InvoiceDocumentTableFormSet,
            'template': 'invoice_document_form_new.html',
            'excel': create_invoice_excel,
            'redirect': 'invoice_document'
        },
        'utd': {
            'model': UtdDocument,
            'form': UtdDocumentForm,
            'formset': UtdDocumentTableFormSet,
            'template': 'utd_document_form_new.html',
            'excel': create_utd_excel,
            'redirect': 'utd_document'
        },
        'vat_invoice': {
            'model': VatInvoiceDocument,
            'form': VatInvoiceDocumentForm,
            'formset': UtdDocumentTableFormSet,
            'template': 'vat_invoice_document_form_new.html',
            'excel': create_vat_invoice_excel,
            'redirect': 'vat_invoice_document'
        },
        'commercial_offer': {
            'model': CommercialOfferDocument,
            'form': CommercialOfferDocumentForm,
            'formset': CommercialOfferDocumentTableFormSet,
            'template': 'commercial_offer_document_form_new.html',
            'excel': create_commercial_offer_excel,
            'redirect': 'commercial_offer_document'
        },
        'outlay': {
            'model': OutlayDocument,
            'form': OutlayDocumentForm,
            'formset': CommercialOfferDocumentTableFormSet,
            'template': 'outlay_document_form_new.html',
            'excel': create_outlay_excel,
            'redirect': 'outlay_document'
        },
        'ks-2': {
            'model': Ks2Document,
            'form': Ks2DocumentForm,
            'formset': Ks2DocumentTableFormSet,
            'template': 'ks2_document_form_new.html',
            'excel': create_ks2_excel,
            'redirect': 'ks_2_document'
        },
        'ks-3': {
            'model': Ks3Document,
            'form': Ks3DocumentForm,
            'formset': Ks3DocumentTableFormSet,
            'template': 'ks3_document_form_new.html',
            'excel': create_ks3_excel,
            'redirect': 'ks_3_document'
        },
        'act_service': {
            'model': ActServiceDocument,
            'form': ActServiceDocumentForm,
            'formset': CommercialOfferDocumentTableFormSet,
            'template': 'act_service_document_form_new.html',
            'excel': create_act_service_excel,
            'redirect': 'act_service_document'
        },
        'power_attorney': {
            'model': PowerAttorneyDocument,
            'form': PowerAttorneyDocumentForm,
            'formset': PowerAttorneyDocumentTableFormSet,
            'template': 'power_attorney_document_form_new.html',
            'excel': create_power_attorney_excel,
            'redirect': 'power_attorney_document'
        },
        'sales_receipt': {
            'model': SalesReceiptDocument,
            'form': SalesReceiptDocumentForm,
            'formset': SalesReceiptDocumentTableFormSet,
            'template': 'sales_receipt_document_form_new.html',
            'excel': create_sales_receipt_excel,
            'redirect': 'sales_receipt_document'
        },
        'pko': {
            'model': PkoDocument,
            'form': PkoDocumentForm,
            'template': 'pko_document_form_new.html',
            'excel': create_pko_excel,
            'redirect': 'pko_document'
        },
        'rko': {
            'model': RkoDocument,
            'form': RkoDocumentForm,
            'template': 'rko_document_form_new.html',
            'excel': create_rko_excel,
            'redirect': 'rko_document'
        },
        'reconciliation': {
            'model': ReconciliationDocument,
            'form': ReconciliationDocumentForm,
            'formset': ReconciliationDocumentTableFormSet,
            'template': 'reconciliation_form_new.html',
            'excel': create_reconciliation_excel,
            'redirect': 'reconciliation_document'
        },
        'agreement': {
            'model': AgreementDocument,
            'form': AgreementDocumentForm,
            'template': 'agreement_document_form_new.html',
            'excel': create_agreement_excel,
            'redirect': 'agreement_document'
        },
    }

    if doc_type not in document_mapping:
        return redirect('error_page')

    document_info = document_mapping[doc_type]
    document_model = document_info['model']
    form_class = document_info['form']
    formset_class = document_info['formset'] if 'formset' in document_info else None
    template_name = document_info['template']
    excel = document_info['excel']

    document = get_object_or_404(document_model, id=id_doc)

    form = form_class(request.POST or None, instance=document, request=request)

    if formset_class:
        table_queryset = document.table_product.all()
        formset = formset_class(request.POST or None, queryset=table_queryset)
    else:
        formset = None

    if request.method == 'POST' and form.is_valid() and (not formset_class or formset.is_valid()):
        form.save()

        formset_data = []
        if formset_class:
            for form_s in formset:
                formset_data.append(form_s.cleaned_data)

        if formset_class:
            id_not_deleted = []
            for form_s in formset:
                if form_s.cleaned_data['id']:
                    id_not_deleted.append(form_s.cleaned_data['id'].id)

            tables = document.table_product.all()
            for table in tables:
                if table.id in id_not_deleted:
                    continue
                else:
                    table.delete()

            tables = formset.save(commit=False)

            for table in tables:
                table.save()
            document.table_product.add(*tables)

        if request.POST.get("download_excel") == "true":
            if doc_type == 'invoice':
                organization_data = {
                    "name": form.cleaned_data['organization'].naming,
                    "inn": form.cleaned_data['organization'].inn,
                    "kpp": form.cleaned_data['organization'].kpp,
                    "ogrn": form.cleaned_data['organization'].ogrn,
                    "address": form.cleaned_data['organization'].address,
                    "phone": form.cleaned_data['organization'].phone,
                    "position_at_work": form.cleaned_data['organization'].position_at_work,
                    "supervisor": form.cleaned_data['organization'].supervisor,
                    "accountant": form.cleaned_data['organization'].accountant,
                    "code_company": form.cleaned_data['organization'].code_company,
                }
                response = excel(form.cleaned_data, organization_data, formset_data)
            else:
                response = excel(form.cleaned_data, formset_data)
            return response

        if request.POST.get("download_pdf") == "true":
            if doc_type == 'invoice':
                organization_data = {
                    "name": form.cleaned_data['organization'].naming,
                    "inn": form.cleaned_data['organization'].inn,
                    "kpp": form.cleaned_data['organization'].kpp,
                    "ogrn": form.cleaned_data['organization'].ogrn,
                    "address": form.cleaned_data['organization'].address,
                    "phone": form.cleaned_data['organization'].phone,
                    "position_at_work": form.cleaned_data['organization'].position_at_work,
                    "supervisor": form.cleaned_data['organization'].supervisor,
                    "accountant": form.cleaned_data['organization'].accountant,
                    "code_company": form.cleaned_data['organization'].code_company,
                }
                response = excel(form.cleaned_data, organization_data, formset_data, True)
            elif doc_type == 'agreement':
                template_name = form.cleaned_data.get('sample')
                template_sample = TemplateDocument.objects.filter(title=template_name).first()
                labels = template_sample.labels.all()

                list_value_dop_field = []

                for label in labels:
                    label_code = request.POST.get(f'{label.label_code}')
                    if label_code:
                        value_label, created = ValueLabel.objects.update_or_create(
                            label=label,
                            value=label_code,
                            defaults={
                                'value': label_code,
                            }
                        )
                        if created:
                            value_label.save()

                        list_value_dop_field.append(value_label)

                document.dop_field.clear()
                document.dop_field.add(*list_value_dop_field)

                context = {
                    'title': template_sample.title,
                    'content': template_sample.content
                }

                html_string = render_to_string('supply_contract.html', context)

                dop_fields = document.dop_field.all()

                for label in labels:
                    value_label = dop_fields.filter(label=label).first()
                    if value_label:
                        html_string = html_string.replace(label.label_code, value_label.value)

                for label in labels:
                    if label.label_code == '{date_doc}':
                        html_string = html_string.replace(label.label_code, str(form.cleaned_data['date']))
                    elif label.label_code == '{number_doc}':
                        html_string = html_string.replace(label.label_code, form.cleaned_data['name'])
                    elif label.label_code == '{name}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['organization'].naming)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{address}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['organization'].address)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{inn}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].inn)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{kpp}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].kpp)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{ogrn}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].ogrn)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{phone}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].phone)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{bank_schet}':
                        if form.cleaned_data['bank_organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['bank_organization'].namimg)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{bank_bik}':
                        if form.cleaned_data['bank_organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['bank_organization'].bic)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{bank_korr}':
                        if form.cleaned_data['bank_organization']:
                            html_string = html_string.replace(label.label_code, form.cleaned_data[
                                'bank_organization'].correspondent_account)
                        else:
                            html_string = html_string.replace(label.label_code,
                                                              '')
                    elif label.label_code == '{org_caption_director}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['organization'].position_at_work)
                        else:
                            html_string = html_string.replace(label.label_code,
                                                              '')
                    elif label.label_code == '{org_director}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['organization'].supervosor)
                        else:
                            html_string = html_string.replace(label.label_code, '')
                    elif label.label_code == '{org_buh}':
                        if form.cleaned_data['organization']:
                            html_string = html_string.replace(label.label_code,
                                                              form.cleaned_data['organization'].accountant)
                        else:
                            html_string = html_string.replace(label.label_code, '')

                organization = form.cleaned_data['organization']
                is_stamp = form.cleaned_data['is_stamp']

                response = excel(html_string, organization, is_stamp, True)
            else:
                response = excel(form.cleaned_data, formset_data, True)
            return response

        if doc_type == 'invoice':
            organization_data = {
                "name": form.cleaned_data['organization'].naming,
                "inn": form.cleaned_data['organization'].inn,
                "kpp": form.cleaned_data['organization'].kpp,
                "ogrn": form.cleaned_data['organization'].ogrn,
                "address": form.cleaned_data['organization'].address,
                "phone": form.cleaned_data['organization'].phone,
                "position_at_work": form.cleaned_data['organization'].position_at_work,
                "supervisor": form.cleaned_data['organization'].supervisor,
                "accountant": form.cleaned_data['organization'].accountant,
                "code_company": form.cleaned_data['organization'].code_company,
            }
            return excel(form.cleaned_data, organization_data, formset_data, True, True)
        elif doc_type == 'agreement':
            template_name = form.cleaned_data.get('sample')
            template_sample = TemplateDocument.objects.filter(title=template_name).first()
            labels = template_sample.labels.all()

            list_value_dop_field = []

            for label in labels:
                label_code = request.POST.get(f'{label.label_code}')
                if label_code:
                    value_label, created = ValueLabel.objects.update_or_create(
                        label=label,
                        value=label_code,
                        defaults={
                            'value': label_code,
                        }
                    )
                    if created:
                        value_label.save()

                    list_value_dop_field.append(value_label)

            document.dop_field.clear()
            document.dop_field.add(*list_value_dop_field)

            context = {
                'title': template_sample.title,
                'content': template_sample.content
            }

            html_string = render_to_string('supply_contract.html', context)

            dop_fields = document.dop_field.all()

            for label in labels:
                value_label = dop_fields.filter(label=label).first()
                if value_label:
                    html_string = html_string.replace(label.label_code, value_label.value)

            for label in labels:
                if label.label_code == '{date_doc}':
                    html_string = html_string.replace(label.label_code, str(form.cleaned_data['date']))
                elif label.label_code == '{number_doc}':
                    html_string = html_string.replace(label.label_code, form.cleaned_data['name'])
                elif label.label_code == '{name}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].naming)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{address}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].address)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{inn}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].inn)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{kpp}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].kpp)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{ogrn}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].ogrn)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{phone}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].phone)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{bank_schet}':
                    if form.cleaned_data['bank_organization']:
                        html_string = html_string.replace(label.label_code,
                                                          form.cleaned_data['bank_organization'].namimg)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{bank_bik}':
                    if form.cleaned_data['bank_organization']:
                        html_string = html_string.replace(label.label_code, form.cleaned_data['bank_organization'].bic)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{bank_korr}':
                    if form.cleaned_data['bank_organization']:
                        html_string = html_string.replace(label.label_code,
                                                          form.cleaned_data['bank_organization'].correspondent_account)
                    else:
                        html_string = html_string.replace(label.label_code,
                                                          '')
                elif label.label_code == '{org_caption_director}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code,
                                                          form.cleaned_data['organization'].position_at_work)
                    else:
                        html_string = html_string.replace(label.label_code,
                                                          '')
                elif label.label_code == '{org_director}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code,
                                                          form.cleaned_data['organization'].supervosor)
                    else:
                        html_string = html_string.replace(label.label_code, '')
                elif label.label_code == '{org_buh}':
                    if form.cleaned_data['organization']:
                        html_string = html_string.replace(label.label_code,
                                                          form.cleaned_data['organization'].accountant)
                    else:
                        html_string = html_string.replace(label.label_code, '')

            organization = form.cleaned_data['organization']
            is_stamp = form.cleaned_data['is_stamp']

            return excel(html_string, organization, is_stamp)
        else:
            return excel(form.cleaned_data, formset_data, True, True)
    return render(request, template_name, {
        'form': form,
        'formset': formset,
        'org_form': OrganizationForm(prefix='organization'),
        'bank_form': BankDetailsOrganizationForm(prefix='bank'),
        'counterparty_form': CounterpartyForm(prefix='counterparty'),
        'counterparty_bank_form': BankCounterpartyForm(prefix='counterparty_bank'),
    })


def find_company_by_inn(request):
    # inn = request.GET.get("inn")
    # if not inn:
    #     return JsonResponse({"success": False, "error": "ИНН не указан"}, status=400)
    #
    # fns_url = f"https://api-fns.ru/api/egr?req={inn}&key=0e1ed851511ec34bdc069ef66f1278e6495d646a"
    # response = requests.get(fns_url)
    #
    # if response.status_code == 200:
    #     data = response.json()
    #     if "items" in data:
    #         company_data = data["items"][0]
    #
    #         if "ЮЛ" in company_data:
    #             company = company_data["ЮЛ"]
    #             return JsonResponse({
    #                 "success": True,
    #                 "type": "Юридическое лицо",
    #                 "name": company.get("НаимСокрЮЛ", ""),
    #                 "kpp": company.get("КПП", ""),
    #                 "ogrn": company.get("ОГРН", ""),
    #                 "address": company.get("Адрес", {}).get("АдресПолн", ""),
    #                 "position_at_work": company.get("Руководитель", {}).get("Должн", ""),
    #                 "supervisor": company.get("Руководитель", {}).get("ФИОПолн", ""),
    #             })
    #
    #         elif "ИП" in company_data:
    #             company = company_data["ИП"]
    #             address = company.get("Адрес", "")
    #             if address:
    #                 address_all = address.get("АдресПолн", "")
    #             else:
    #                 address_all = address
    #             return JsonResponse({
    #                 "success": True,
    #                 "type": "Индивидуальный предприниматель",
    #                 "name": company.get("ФИОПолн", ""),
    #                 "ogrn": company.get("ОГРНИП", ""),
    #                 "address": address_all,
    #             })
    #
    # return JsonResponse({"success": False, "error": "Компания или ИП не найдены"}, status=404)

    inn = request.GET.get("inn")

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": inn}

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            if result["suggestions"]:
                company_info = result["suggestions"][0]["data"]
                if company_info["opf"]["short"] not in 'ИП':
                    name_company = result["suggestions"][0]["value"]
                    address = company_info["address"].get("value", "")
                    position_at_work = company_info["management"].get("post", "")
                    supervisor = company_info["management"].get("name", "")
                    return JsonResponse({
                                    "success": True,
                                    "type": "Юридическое лицо",
                                    "name": name_company,
                                    "kpp": company_info.get("kpp", ""),
                                    "ogrn": company_info.get("ogrn", ""),
                                    "address": address,
                                    "position_at_work": position_at_work,
                                    "supervisor": supervisor,
                                })
                elif company_info["opf"]["short"] == "ИП":
                    name_company = result["suggestions"][0]["value"]
                    address = company_info["address"].get("value", "")
                    return JsonResponse({
                                    "success": True,
                                    "type": "Индивидуальный предприниматель",
                                    "name": name_company,
                                    "ogrn": company_info.get("ogrn", ""),
                                    "address": address,
                                })

    except requests.RequestException as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


DADATA_API_KEY = "bb47885575aa2239d036af551ba88f3da668d266"


def find_bank_by_bik(request):
    bik = request.GET.get("bik")
    if not bik:
        return JsonResponse({"success": False, "error": "БИК не указан"}, status=400)

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/bank"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": bik}

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            if result["suggestions"]:
                bank_info = result["suggestions"][0]["data"]
                return JsonResponse({
                    "success": True,
                    "bank_name": bank_info.get("name", {}).get("payment", ""),
                    "address": bank_info.get("address", {}).get("value", ""),
                    "correspondent_account": bank_info.get("correspondent_account", ""),

                })
            else:
                return JsonResponse({"success": False, "error": "Банк не найден"}, status=404)
        else:
            return JsonResponse({"success": False, "error": "Ошибка Dadata API"}, status=response.status_code)

    except requests.RequestException as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def inn_autocomplete(request):
    query = request.GET.get('query', '').strip()

    if len(query) < 3:
        return JsonResponse({"suggestions": []})

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
    headers = {
        "Authorization": f"Token {DADATA_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "query": query,
        "count": 5,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        results = response.json().get("suggestions", [])
        suggestions = [{"value": item["value"], "inn": item["data"]["inn"]} for item in results if item["data"]["state"]["status"] == 'ACTIVE']
        return JsonResponse({"suggestions": suggestions})

    return JsonResponse({"suggestions": []})


def bank_autocomplete(request):
    query = request.GET.get('query', '').strip()

    if len(query) < 3:
        return JsonResponse({"suggestions": []})

    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/bank"
    headers = {
        "Authorization": f"Token {DADATA_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "query": query,
        "count": 5,
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        results = response.json().get("suggestions", [])
        suggestions = [{"value": item["value"], "inn": item["data"]["bic"]} for item in results]
        return JsonResponse({"suggestions": suggestions})

    return JsonResponse({"suggestions": []})


def print_document(request, doc_type, document_id):
    models_doc_type = {
        'invoice': {
            'model': InvoiceDocument,
            'form': InvoiceDocumentForm,
            'formset': InvoiceDocumentTableFormSet,
            'excel': create_invoice_excel
        },
        'utd': {
            'model': UtdDocument,
            'form': UtdDocumentForm,
            'formset': UtdDocumentTableFormSet,
            'excel': create_utd_excel
        },
        'vat_invoice': {
            'model': VatInvoiceDocument,
            'form': VatInvoiceDocumentForm,
            'formset': UtdDocumentTableFormSet,
            'excel': create_vat_invoice_excel,
        },
        'commercial_offer': {
            'model': CommercialOfferDocument,
            'form': CommercialOfferDocumentForm,
            'formset': CommercialOfferDocumentTableFormSet,
            'excel': create_commercial_offer_excel,
        },
        'outlay': {
            'model': OutlayDocument,
            'form': OutlayDocumentForm,
            'formset': CommercialOfferDocumentTableFormSet,
            'excel': create_outlay_excel,
        },
        'ks-2': {
            'model': Ks2Document,
            'form': Ks2DocumentForm,
            'formset': Ks2DocumentTableFormSet,
            'excel': create_ks2_excel,
        },
        'ks-3': {
            'model': Ks3Document,
            'form': Ks3DocumentForm,
            'formset': Ks3DocumentTableFormSet,
            'excel': create_ks3_excel,
        },
        'act_service': {
            'model': ActServiceDocument,
            'form': ActServiceDocumentForm,
            'formset': CommercialOfferDocumentTableFormSet,
            'excel': create_act_service_excel,
        },
        'power_attorney': {
            'model': PowerAttorneyDocument,
            'form': PowerAttorneyDocumentForm,
            'formset': PowerAttorneyDocumentTableFormSet,
            'excel': create_power_attorney_excel,
        },
        'sales_receipt': {
            'model': SalesReceiptDocument,
            'form': SalesReceiptDocumentForm,
            'formset': SalesReceiptDocumentTableFormSet,
            'excel': create_sales_receipt_excel,
        },
        'pko': {
            'model': PkoDocument,
            'form': PkoDocumentForm,
            'excel': create_pko_excel,
        },
        'rko': {
            'model': RkoDocument,
            'form': RkoDocumentForm,
            'excel': create_rko_excel,
        },
        'reconciliation': {
            'model': ReconciliationDocument,
            'form': ReconciliationDocumentForm,
            'formset': ReconciliationDocumentTableFormSet,
            'excel': create_reconciliation_excel,
        },
        'agreement': {
            'model': AgreementDocument,
            'form': AgreementDocumentForm,
            'excel': create_agreement_excel,
        },
    }

    document = get_object_or_404(models_doc_type[doc_type]['model'], id=document_id)

    form = models_doc_type[doc_type]['form'](instance=document)

    if doc_type not in ['pko', 'rko', 'agreement']:
        formset = models_doc_type[doc_type]['formset'](queryset=document.table_product.all())
    else:
        formset = []

    form_data = {field.name: getattr(form.instance, field.name) for field in form.instance._meta.get_fields()}

    formset_data = []
    for form_s in formset:
        forms_data = {field.name: field.value() for field in form_s}
        formset_data.append(forms_data)

    if doc_type == 'invoice':
        organization_data = {
            "name": form_data['organization'].naming,
            "inn": form_data['organization'].inn,
            "kpp": form_data['organization'].kpp,
            "ogrn": form_data['organization'].ogrn,
            "address": form_data['organization'].address,
            "phone": form_data['organization'].phone,
            "position_at_work": form_data['organization'].position_at_work,
            "supervisor": form_data['organization'].supervisor,
            "accountant": form_data['organization'].accountant,
            "code_company": form_data['organization'].code_company,
        }
        return models_doc_type[doc_type]['excel'](form_data, organization_data, formset_data, True, True)

    elif doc_type == 'agreement':
        template_name = form_data['sample']
        template_sample = TemplateDocument.objects.filter(title=template_name).first()

        labels = template_sample.labels.all()

        context = {
            'title': template_sample.title,
            'content': template_sample.content
        }

        html_string = render_to_string('supply_contract.html', context)

        dop_fields = document.dop_field.all()

        for label in labels:
            value_label = dop_fields.filter(label=label).first()
            if value_label:
                html_string = html_string.replace(label.label_code, value_label.value)

        for label in labels:
            if label.label_code == '{date_doc}':
                html_string = html_string.replace(label.label_code, str(form_data['date']))
            elif label.label_code == '{number_doc}':
                html_string = html_string.replace(label.label_code, form_data['name'])
            elif label.label_code == '{name}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].naming)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{address}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].address)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{inn}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].inn)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{kpp}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].kpp)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{ogrn}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].ogrn)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{phone}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].phone)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_schet}':
                if form_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form_data['bank_organization'].namimg)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_bik}':
                if form_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form_data['bank_organization'].bic)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_korr}':
                if form_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form_data['bank_organization'].correspondent_account)
                else:
                    html_string = html_string.replace(label.label_code,
                                                      '')
            elif label.label_code == '{org_caption_director}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].position_at_work)
                else:
                    html_string = html_string.replace(label.label_code,
                                                      '')
            elif label.label_code == '{org_director}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].supervosor)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{org_buh}':
                if form_data['organization']:
                    html_string = html_string.replace(label.label_code, form_data['organization'].accountant)
                else:
                    html_string = html_string.replace(label.label_code, '')

        organization = form_data['organization']
        is_stamp = form_data['is_stamp']

        return models_doc_type[doc_type]['excel'](html_string, organization, is_stamp)

    return models_doc_type[doc_type]['excel'](form_data, formset_data, True, True)


def add_template_document(request):
    labels = LabelTemplateDocument.objects.all()

    if request.method == 'POST':
        form = TemplateDocumentForm(request.POST)
        if form.is_valid():
            template_document = form.save(commit=False)

            template_document.save()

            for label in labels:
                if label.label_code in form.cleaned_data['content']:
                    template_document.labels.add(label)

            template_document.save()

            return redirect('agreement_document')
    else:
        form = TemplateDocumentForm()

    return render(request, 'add_template_document.html', {'form': form, 'labels': labels})


def get_labels(request):
    not_labels = ['{date_doc}', '{number_doc}', '{name}', '{address}', '{inn}', '{kpp}', '{ogrn}', '{phone}', '{bank_schet}', '{bank_bik}', '{bank_korr}', '{org_caption_director}', '{org_director}', '{org_buh}']

    sample_id = request.GET.get('sample_id')
    if sample_id:
        document = TemplateDocument.objects.filter(title=sample_id).first()

        labels_data = [{'id': label.id, 'name': label.label_desc, 'code': label.label_code} for label in document.labels.all() if label.label_code not in not_labels]

        return JsonResponse({'labels': labels_data})
    else:
        return JsonResponse({'labels': []})


def get_value_labels(request):
    document_name = request.GET.get('sample_id')
    if not document_name:
        return JsonResponse({}, status=400)

    try:
        document = AgreementDocument.objects.get(name=document_name)
        labels = document.dop_field.all()
        saved_values = {
            label.label.label_code: label.value for label in labels
        }
        return JsonResponse({"values": saved_values})
    except AgreementDocument.DoesNotExist:
        return JsonResponse({}, status=404)