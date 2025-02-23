from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from invoice.models import RkoDocument
from .forms import RkoDocumentForm
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from rko.utils.excel import create_rko_excel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date


class RkoDocumentCreateView(LoginRequiredMixin, CreateView):
    model = RkoDocument
    form_class = RkoDocumentForm
    template_name = 'rko_document_form_new.html'
    success_url = reverse_lazy('rko_document')

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

        return context

    def form_valid(self, form):
        document_name = form.cleaned_data.get('name')
        document_date = form.cleaned_data.get('date')
        existing_document = RkoDocument.objects.filter(name=document_name, date=document_date)
        if existing_document:
            self.object = form.save(commit=False)
            self.object.pk = existing_document.first().pk
            self.object.user = self.request.user
            self.object.save()
        else:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()

        if self.request.POST.get("download_excel") == "true":
            form_data = form.cleaned_data
            response = create_rko_excel(form_data, [])
            return response

        if self.request.POST.get("download_pdf") == "true":
            form_data = form.cleaned_data
            response = create_rko_excel(form_data, [], True)
            return response

        form_data = form.cleaned_data
        response = create_rko_excel(form_data, [], True, True)
        return response


def rko_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    documents = RkoDocument.objects.select_related('organization').filter(user=request.user)

    if query:
        documents = documents.filter(name__icontains=query)

    if date_from:
        documents = documents.filter(date__gte=parse_date(date_from))
    if date_to:
        documents = documents.filter(date__lte=parse_date(date_to))

    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST' and 'delete_document' in request.POST:
        document_id = request.POST.get('document_id')
        document = RkoDocument.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('rko_document')

    return render(request, 'rko_document_new.html',
                  {'page_obj': page_obj, 'query': query, 'date_from': date_from, 'date_to': date_to})
