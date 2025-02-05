from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm, \
    InvoiceDocumentForm, InvoiceDocumentTableFormSet
from invoice.models import InformationOrganization, Buyer, InvoiceDocument, BankDetailsOrganization, BankDetailsBuyer, \
    InvoiceDocumentTable, UtdDocument, VatInvoiceDocument
from collections import defaultdict
import requests
from django.http import JsonResponse


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
    return render(request, 'profile.html',
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

        if org_form.is_valid() and bank_form.is_valid():
            organization = org_form.save(commit=False)
            organization.user = request.user
            organization.save()

            bank_details = bank_form.save(commit=False)
            bank_details.organization = organization
            bank_details.save()

            return redirect('profile')
        else:
            return render(request, 'add_organization.html', {
                'org_form': org_form,
                'bank_form': bank_form
            })
    else:
        return render(request, 'add_organization.html',
                      {'org_form': OrganizationForm(prefix='organization'),
                       'bank_form': BankDetailsOrganizationForm(prefix='bank')})


def add_counterparty_from_profile(request):
    if request.method == 'POST':
        counterparty_form = CounterpartyForm(request.POST, prefix='counterparty')
        counterparty_bank_form = BankCounterpartyForm(request.POST, prefix='counterparty_bank')

        if counterparty_form.is_valid() and counterparty_bank_form.is_valid():
            counterparty = counterparty_form.save(commit=False)
            counterparty.user = request.user
            counterparty.save()

            counterparty_bank = counterparty_bank_form.save(commit=False)
            counterparty_bank.organization = counterparty
            counterparty_bank.save()

            return redirect('profile')
        else:
            errors = counterparty_form.errors.as_json() + counterparty_bank_form.errors.as_json()
            print(errors)

            return 'Error'
    else:
        return render(request, 'add_counterparty.html',
                      {'counterparty_form': CounterpartyForm(prefix='counterparty'),
                       'counterparty_bank_form': BankCounterpartyForm(prefix='counterparty_bank')})


@login_required
def edit_organization(request, id_org):
    organization = InformationOrganization.objects.get(id=id_org)
    bank_details = BankDetailsOrganization.objects.filter(organization=organization).first()

    if request.method == 'POST':
        org_form = OrganizationForm(request.POST, request.FILES, instance=organization, prefix='organization')
        bank_form = BankDetailsOrganizationForm(request.POST, instance=bank_details, prefix='bank')

        if org_form.is_valid() and bank_form.is_valid():
            org_form.save()
            bank_form.save()

            return redirect('profile')

    else:
        org_form = OrganizationForm(instance=organization, prefix='organization')
        bank_form = BankDetailsOrganizationForm(instance=bank_details, prefix='bank')

    return render(request, 'add_organization.html', {
        'org_form': org_form,
        'bank_form': bank_form,
    })


@login_required
def edit_counterparty(request, id_org):
    counterparty = Buyer.objects.get(id=id_org)
    bank_details_counterparty = BankDetailsBuyer.objects.filter(organization=counterparty).first()

    if request.method == 'POST':
        org_form = CounterpartyForm(request.POST, instance=counterparty, prefix='counterparty')
        bank_form = BankCounterpartyForm(request.POST, instance=bank_details_counterparty, prefix='counterparty_bank')

        if org_form.is_valid() and bank_form.is_valid():
            org_form.save()
            bank_form.save()

            return redirect('profile')

    else:
        org_form = CounterpartyForm(instance=counterparty, prefix='counterparty')
        bank_form = BankCounterpartyForm(instance=bank_details_counterparty, prefix='counterparty_bank')

    return render(request, 'add_counterparty.html', {
        'counterparty_form': org_form,
        'counterparty_bank_form': bank_form,
    })


@login_required
def edit_document(request, id_doc):
    document = InvoiceDocument.objects.get(id=id_doc)
    form = InvoiceDocumentForm(request.POST or None, instance=document)

    invoice_document_table_queryset = document.table_product.all()
    formset = InvoiceDocumentTableFormSet(request.POST or None, queryset=invoice_document_table_queryset)

    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        form.save()

        invoice_tables = formset.save(commit=False)

        for invoice_table in invoice_tables:
            invoice_table.save()

        document.table_product.add(*invoice_tables)

        return redirect('profile')

    return render(request, 'invoice_document_form.html',
                  {
                      'form': form,
                      'org_form': OrganizationForm(prefix='organization'),
                      'bank_form': BankDetailsOrganizationForm(prefix='bank'),
                      'counterparty_form': CounterpartyForm(prefix='counterparty'),
                      'counterparty_bank_form': BankCounterpartyForm(prefix='counterparty_bank'),
                      'formset': formset

                  })


def find_company_by_inn(request):
    inn = request.GET.get("inn")
    if not inn:
        return JsonResponse({"success": False, "error": "ИНН не указан"}, status=400)

    fns_url = f"https://api-fns.ru/api/egr?req={inn}&key=98843b355dc4b54850fd0237db59abd77fa5237c"
    response = requests.get(fns_url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            company = data["items"][0]
            return JsonResponse({
                "success": True,

                "name": company.get("ЮЛ", {}).get("НаимСокрЮЛ", ""),
                "kpp": company.get("ЮЛ", {}).get("КПП", ""),
                "ogrn": company.get("ЮЛ", {}).get("ОГРН", ""),
                "address": company.get("ЮЛ", {}).get("Адрес", {}).get("АдресПолн", ""),
                "position_at_work": company.get("ЮЛ", {}).get("Руководитель", {}).get("Должн", ""),
                "supervisor": company.get("ЮЛ", {}).get("Руководитель", {}).get("ФИОПолн", ""),
            })
    return JsonResponse({"success": False, "error": "Компания не найдена"}, status=404)


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
