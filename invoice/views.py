from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import InvoiceDocument, InvoiceDocumentTable, BankDetailsOrganization, InformationOrganization, Buyer, \
    BankDetailsBuyer
from .forms import InvoiceDocumentForm, OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, \
    BankCounterpartyForm, InvoiceDocumentTableFormSet
from django.shortcuts import redirect, render
from invoice.utils.excel import create_invoice_excel
from django.contrib.auth.mixins import LoginRequiredMixin


class InvoiceDocumentCreateView(LoginRequiredMixin, CreateView):
    model = InvoiceDocument
    form_class = InvoiceDocumentForm
    template_name = 'invoice_document_form.html'
    success_url = reverse_lazy('invoice')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['org_form'] = OrganizationForm(prefix='organization')
        context['bank_form'] = BankDetailsOrganizationForm(prefix='bank')
        context['counterparty_form'] = CounterpartyForm(prefix='counterparty')
        context['counterparty_bank_form'] = BankCounterpartyForm(prefix='counterparty_bank')
        context['formset'] = InvoiceDocumentTableFormSet(queryset=InvoiceDocumentTable.objects.none())

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        organization_data = {
            "name": self.object.organization.naming,
            "inn": self.object.organization.inn,
            "kpp": self.object.organization.kpp,
            "ogrn": self.object.organization.ogrn,
            "address": self.object.organization.address,
            "phone": self.object.organization.phone,
            "position_at_work": self.object.organization.position_at_work,
            "supervisor": self.object.organization.supervisor,
            "accountant": self.object.organization.accountant,
            "code_company": self.object.organization.code_company,
        }

        formset = InvoiceDocumentTableFormSet(self.request.POST)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'name': form_s.cleaned_data.get('name'),
                    'unit_of_measurement': form_s.cleaned_data.get('unit_of_measurement'),
                    'quantity': form_s.cleaned_data.get('quantity'),
                    'price': form_s.cleaned_data.get('price'),
                    'amount': form_s.cleaned_data.get('amount'),
                    'discount': form_s.cleaned_data.get('discount')
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            form_data = form.cleaned_data

            response = create_invoice_excel(form_data, organization_data, formset_data)

            return response
        else:
            print(formset.errors)
            return redirect('/')


def add_organization(request):
    if request.method == 'POST':
        org_form = OrganizationForm(request.POST, prefix='organization')
        bank_form = BankDetailsOrganizationForm(request.POST, prefix='bank')

        if org_form.is_valid() and bank_form.is_valid():
            organization = org_form.save()

            bank_details = bank_form.save(commit=False)
            bank_details.organization = organization
            bank_details.save()

            return JsonResponse(
                {
                    'name': organization.naming,
                    'id': organization.id,
                    'bank_name': bank_details.naming,
                    'bank_id': bank_details.id
                }
            )
        else:
            errors = org_form.errors.as_json() + bank_form.errors.as_json()
            return JsonResponse({'errors': errors})


def add_counterparty(request):
    if request.method == 'POST':
        counterparty_form = CounterpartyForm(request.POST, prefix='counterparty')
        counterparty_bank_form = BankCounterpartyForm(request.POST, prefix='counterparty_bank')

        if counterparty_form.is_valid() and counterparty_bank_form.is_valid():
            counterparty = counterparty_form.save()

            counterparty_bank = counterparty_bank_form.save(commit=False)
            counterparty_bank.organization = counterparty
            counterparty_bank.save()

            return JsonResponse(
                {
                    'name': counterparty.naming,
                    'id': counterparty.id,
                    'bank_name': counterparty_bank.naming,
                    'bank_id': counterparty_bank.id
                }
            )
        else:
            errors = counterparty_form.errors.as_json() + counterparty_bank_form.errors.as_json()
            return JsonResponse({'errors': errors})


def pdf(request):
    return render(request, 'invoice_template.html')


def get_banks(request):
    organization_id = request.GET.get('organization_id')
    if organization_id:
        organization = InformationOrganization.objects.get(id=organization_id)
        banks = BankDetailsOrganization.objects.filter(organization=organization).select_related('organization').values(
            'id', 'naming', 'organization__naming')
        return JsonResponse({'banks': list(banks)})
    return JsonResponse({'banks': [{'id': '', 'naming': ''}]})


def get_banks_counterparty(request):
    organization_id = request.GET.get('organization_id')
    if organization_id:
        organization = Buyer.objects.get(id=organization_id)
        banks = BankDetailsBuyer.objects.filter(organization=organization).select_related('organization').values(
            'id', 'naming', 'organization__naming')
        return JsonResponse({'banks': list(banks)})
    return JsonResponse({'banks': [{'id': '', 'naming': ''}]})


def generate_invoice_excel(request):
    form = InvoiceDocumentForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        print(form_data)
        return redirect('/')
        # return create_invoice_excel(form_data)
    else:
        print('Ошибка валидации формы:', form.errors)
        return redirect('/')
