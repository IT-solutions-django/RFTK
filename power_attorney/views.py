from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from invoice.models import PowerAttorneyDocument, PowerAttorneyDocumentTable
from .forms import PowerAttorneyDocumentForm, PowerAttorneyDocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from power_attorney.utils.excel import create_power_attorney_excel


class PowerAttorneyDocumentCreateView(LoginRequiredMixin, CreateView):
    model = PowerAttorneyDocument
    form_class = PowerAttorneyDocumentForm
    template_name = 'power_attorney_document_form.html'
    success_url = reverse_lazy('power-attorney')

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
        context['formset'] = PowerAttorneyDocumentTableFormSet(queryset=PowerAttorneyDocumentTable.objects.none())

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = PowerAttorneyDocumentTableFormSet(self.request.POST)

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
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            form_data = form.cleaned_data

            response = create_power_attorney_excel(form_data, formset_data)

            return response
