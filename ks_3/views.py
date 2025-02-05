from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from invoice.models import Ks3Document, Ks3DocumentTable
from .forms import Ks3DocumentForm, Ks3DocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from commercial_offer.utils.excel import create_commercial_offer_excel


class Ks3DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Ks3Document
    form_class = Ks3DocumentForm
    template_name = 'ks3_document_form.html'
    success_url = reverse_lazy('ks3')

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
        context['formset'] = Ks3DocumentTableFormSet(queryset=Ks3DocumentTable.objects.none())

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = Ks3DocumentTableFormSet(self.request.POST)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'name': form_s.cleaned_data.get('name'),
                    'code': form_s.cleaned_data.get('code'),
                    'quantity': form_s.cleaned_data.get('quantity'),
                    'price': form_s.cleaned_data.get('price'),
                    'price_from_construction': form_s.cleaned_data.get('price_from_construction'),
                    'price_from_year': form_s.cleaned_data.get('price_from_year'),
                    'amount': form_s.cleaned_data.get('amount'),
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            form_data = form.cleaned_data

            response = create_commercial_offer_excel(form_data, formset_data)

            return response
