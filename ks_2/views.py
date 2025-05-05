from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from invoice.models import Ks2Document, Ks2DocumentTable, InformationOrganization, Buyer
from .forms import Ks2DocumentForm, Ks2DocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from ks_2.utils.excel import create_ks2_excel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from ks_2.utils.ks_2_registry_pdf import create_ks_2_registry_pdf


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
        document_name = form.cleaned_data.get('name')
        document_date = form.cleaned_data.get('date')
        existing_document = Ks2Document.objects.filter(name=document_name, date=document_date)
        if existing_document:
            self.object = form.save(commit=False)
            self.object.pk = existing_document.first().pk
            self.object.user = self.request.user
            self.object.save()
        else:
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

            form_data = form.cleaned_data
            response = create_ks2_excel(form_data, formset_data, True, True)
            return response

        return super().form_valid(form)


def ks_2_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    org_param = request.GET.get('filter_org', '')
    coun_param = request.GET.get('filter_coun', '')
    sort_param = request.GET.get('sort', '')

    documents = Ks2Document.objects.select_related('organization', 'counterparty').prefetch_related('table_product').filter(user=request.user)

    if query:
        documents = documents.filter(name__icontains=query)

    if date_from:
        documents = documents.filter(date__gte=parse_date(date_from))
    if date_to:
        documents = documents.filter(date__lte=parse_date(date_to))
    if org_param:
        documents = documents.filter(organization=org_param)
    if coun_param:
        documents = documents.filter(counterparty=coun_param)

    if request.GET.get('cnt_page_paginator', ''):
        cnt_page = int(request.GET.get('cnt_page_paginator'))
    else:
        cnt_page = 20

    if sort_param:
        if sort_param == 'date_document_new':
            documents = documents.order_by('-date')
        elif sort_param == 'date_document_old':
            documents = documents.order_by('date')
        elif sort_param == 'name_document_new':
            documents = documents.order_by('name')
        elif sort_param == 'name_document_old':
            documents = documents.order_by('-name')
    else:
        documents = documents.order_by('-date')

    paginator = Paginator(documents, cnt_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)

    if request.method == 'POST' and 'delete_document' in request.POST:
        document_id = request.POST.get('document_id')
        document = Ks2Document.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('ks_2_document')

    organizations = InformationOrganization.objects.filter(user=request.user)

    counterparty = Buyer.objects.filter(user=request.user)

    return render(request, 'ks2_document_new.html',
                  {'page_obj': page_obj, 'query': query, 'date_from': date_from, 'date_to': date_to, 'current_page': page_obj.number, 'total_pages': paginator.num_pages, 'organizations': organizations, 'counterparty':  counterparty, 'page_range': page_range})


def ks_2_registry(request):
    utd_documents_all = Ks2Document.objects.select_related('organization', 'counterparty').filter(user=request.user).annotate(
        document_sum=Sum('table_product__amount')
    )

    context = {
        'utd_documents_all': utd_documents_all
    }

    html_string = render_to_string('ks_2_registry.html', context)

    response = create_ks_2_registry_pdf(html_string)
    return response
