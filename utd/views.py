from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from invoice.models import UtdDocument, UtdDocumentTable
from .forms import UtdDocumentForm, UtdDocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from utd.utils.excel import create_utd_excel
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date


class UtdDocumentCreateView(LoginRequiredMixin, CreateView):
    model = UtdDocument
    form_class = UtdDocumentForm
    template_name = 'utd_document_form_new.html'
    success_url = reverse_lazy('utd_document')

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
        context['formset'] = UtdDocumentTableFormSet(queryset=UtdDocumentTable.objects.none())

        return context

    def form_valid(self, form):
        document_name = form.cleaned_data.get('name')
        existing_document = UtdDocument.objects.filter(name=document_name)
        if existing_document:
            self.object = form.save(commit=False)
            self.object.pk = existing_document.first().pk
            self.object.user = self.request.user
            self.object.save()
        else:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

        formset = UtdDocumentTableFormSet(self.request.POST)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'name': form_s.cleaned_data.get('name'),
                    'product_code': form_s.cleaned_data.get('product_code'),
                    'product_type_code': form_s.cleaned_data.get('product_type_code'),
                    'excise': form_s.cleaned_data.get('excise'),
                    'country': form_s.cleaned_data.get('country'),
                    'number_GTD': form_s.cleaned_data.get('number_GTD'),
                    'unit_of_measurement': form_s.cleaned_data.get('unit_of_measurement'),
                    'quantity': form_s.cleaned_data.get('quantity'),
                    'price': form_s.cleaned_data.get('price'),
                    'amount': form_s.cleaned_data.get('amount'),
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            if self.request.POST.get("download_excel") == "true":
                form_data = form.cleaned_data
                response = create_utd_excel(form_data, formset_data)
                return response

            if self.request.POST.get("download_pdf") == "true":
                form_data = form.cleaned_data
                response = create_utd_excel(form_data, formset_data, True)
                return response

            form_data = form.cleaned_data
            response = create_utd_excel(form_data, formset_data, True, True)
            return response

        return super().form_valid(form)


def utd_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    documents = UtdDocument.objects.select_related('organization', 'counterparty').filter(user=request.user)

    if query:
        documents = documents.filter(name__icontains=query)

    if date_from:
        documents = documents.filter(date__gte=parse_date(date_from))
    if date_to:
        documents = documents.filter(date__lte=parse_date(date_to))

    paginator = Paginator(documents, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST' and 'delete_document' in request.POST:
        document_id = request.POST.get('document_id')
        document = UtdDocument.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('utd_document')

    return render(request, 'utd_document_new.html',
                  {'page_obj': page_obj, 'query': query, 'date_from': date_from, 'date_to': date_to})
