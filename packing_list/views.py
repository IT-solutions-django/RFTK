from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import CreateView
from invoice.models import PackingListDocument, PackingListDocumentTable
from .forms import PackingListDocumentForm, PackingListDocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from packing_list.utils.excel import create_packing_list_excel


class PackingListDocumentCreateView(LoginRequiredMixin, CreateView):
    model = PackingListDocument
    form_class = PackingListDocumentForm
    template_name = 'packing_list_document_form.html'
    success_url = reverse_lazy('packing-list')

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
        context['formset'] = PackingListDocumentTableFormSet(queryset=PackingListDocumentTable.objects.none())

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = PackingListDocumentTableFormSet(self.request.POST)

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
                    'product_code': form_s.cleaned_data.get('product_code'),
                    'type_of_packaging': form_s.cleaned_data.get('type_of_packaging'),
                    'gross_weight': form_s.cleaned_data.get('gross_weight'),
                    'net_weight': form_s.cleaned_data.get('net_weight'),
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            form_data = form.cleaned_data

            response = create_packing_list_excel(form_data, formset_data)

            return response
