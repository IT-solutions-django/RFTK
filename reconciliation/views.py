from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from invoice.models import ReconciliationDocument, ReconciliationDocumentTable, InformationOrganization, Buyer
from .forms import ReconciliationDocumentForm, ReconciliationDocumentTableFormSet
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, CounterpartyForm
from reconciliation.utils.excel import create_reconciliation_excel
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from reconciliation.utils.reconciliation_registry_pdf import create_reconciliation_registry_pdf


class ReconciliationCreateView(LoginRequiredMixin, CreateView):
    model = ReconciliationDocument
    form_class = ReconciliationDocumentForm
    template_name = 'reconciliation_form_new.html'
    success_url = reverse_lazy('reconciliation_document')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['org_form'] = OrganizationForm(prefix='organization')
        context['counterparty_form'] = CounterpartyForm(prefix='counterparty')
        context['formset'] = ReconciliationDocumentTableFormSet(queryset=ReconciliationDocumentTable.objects.none())

        return context

    def form_valid(self, form):
        document_name = form.cleaned_data.get('name')
        existing_document = ReconciliationDocument.objects.filter(name=document_name)
        if existing_document:
            self.object = form.save(commit=False)
            self.object.pk = existing_document.first().pk
            self.object.user = self.request.user
            self.object.save()
        else:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

        formset = ReconciliationDocumentTableFormSet(self.request.POST)

        if formset.is_valid():
            invoice_tables = []
            formset_data = []

            for form_s in formset:
                invoice_table = form_s.save(commit=False)
                invoice_table.save()
                invoice_tables.append(invoice_table)

                row_data = {
                    'name_operation_org': form_s.cleaned_data.get('name_operation_org'),
                    'debit_org': form_s.cleaned_data.get('debit_org'),
                    'loan_org': form_s.cleaned_data.get('loan_org'),
                    'name_operation_counterparty': form_s.cleaned_data.get('name_operation_counterparty'),
                    'debit_counterparty': form_s.cleaned_data.get('debit_counterparty'),
                    'loan_counterparty': form_s.cleaned_data.get('loan_counterparty')
                }

                formset_data.append(row_data)

            self.object.table_product.set(invoice_tables)

            if self.request.POST.get("download_excel") == "true":
                form_data = form.cleaned_data
                response = create_reconciliation_excel(form_data, formset_data)
                return response

            if self.request.POST.get("download_pdf") == "true":
                form_data = form.cleaned_data
                response = create_reconciliation_excel(form_data, formset_data, True)
                return response

            form_data = form.cleaned_data
            response = create_reconciliation_excel(form_data, formset_data, True, True)
            return response

        return super().form_valid(form)


def reconciliation_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    org_param = request.GET.get('filter_org', '')
    coun_param = request.GET.get('filter_coun', '')
    sort_param = request.GET.get('sort', '')

    documents = ReconciliationDocument.objects.select_related('organization', 'counterparty').filter(user=request.user)

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
        document = ReconciliationDocument.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('reconciliation_document')

    organizations = InformationOrganization.objects.filter(user=request.user)

    counterparty = Buyer.objects.filter(user=request.user)

    return render(request, 'reconciliation_document_new.html',
                  {'page_obj': page_obj, 'query': query, 'date_from': date_from, 'date_to': date_to, 'current_page': page_obj.number, 'total_pages': paginator.num_pages, 'organizations': organizations, 'counterparty':  counterparty, 'page_range': page_range})


def reconciliation_registry(request):
    utd_documents_all = ReconciliationDocument.objects.select_related('organization', 'counterparty').filter(user=request.user)

    context = {
        'utd_documents_all': utd_documents_all
    }

    html_string = render_to_string('reconciliation_registry.html', context)

    response = create_reconciliation_registry_pdf(html_string)
    return response
