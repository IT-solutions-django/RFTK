from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from invoice.models import Ks2Document, Ks2DocumentTable
from .forms import Ks2DocumentForm, Ks2DocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from ks_2.utils.excel import create_ks2_excel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator


class Ks2DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Ks2Document
    form_class = Ks2DocumentForm
    template_name = 'ks2_document_form_new.html'
    success_url = reverse_lazy('ks_2_document')

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
        context['formset'] = Ks2DocumentTableFormSet(queryset=Ks2DocumentTable.objects.none())

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        formset = Ks2DocumentTableFormSet(self.request.POST)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'name': form_s.cleaned_data.get('name'),
                    'number_outlay': form_s.cleaned_data.get('number_outlay'),
                    'number_unit': form_s.cleaned_data.get('number_unit'),
                    'unit_of_measurement': form_s.cleaned_data.get('unit_of_measurement'),
                    'quantity': form_s.cleaned_data.get('quantity'),
                    'price': form_s.cleaned_data.get('price'),
                    'amount': form_s.cleaned_data.get('amount'),
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            if self.request.POST.get("download_excel") == "true":
                form_data = form.cleaned_data
                response = create_ks2_excel(form_data, formset_data)
                return response

            if self.request.POST.get("download_pdf") == "true":
                form_data = form.cleaned_data
                response = create_ks2_excel(form_data, formset_data, True)
                return response

        return super().form_valid(form)


def ks_2_document(request):
    documents = Ks2Document.objects.select_related('organization', 'counterparty').filter(user=request.user)
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST' and 'delete_document' in request.POST:
        document_id = request.POST.get('document_id')
        document = Ks2Document.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('ks_2_document')

    return render(request, 'ks2_document_new.html', {'page_obj': page_obj})
