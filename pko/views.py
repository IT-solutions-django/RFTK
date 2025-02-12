from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from invoice.models import PkoDocument
from .forms import PkoDocumentForm
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from pko.utils.excel import create_pko_excel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator


class PkoDocumentCreateView(LoginRequiredMixin, CreateView):
    model = PkoDocument
    form_class = PkoDocumentForm
    template_name = 'pko_document_form_new.html'
    success_url = reverse_lazy('pko_document')

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
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        if self.request.POST.get("download_excel") == "true":
            form_data = form.cleaned_data
            response = create_pko_excel(form_data, [])
            return response

        if self.request.POST.get("download_pdf") == "true":
            form_data = form.cleaned_data
            response = create_pko_excel(form_data, [], True)
            return response

        return super().form_valid(form)


def pko_document(request):
    documents = PkoDocument.objects.select_related('organization').filter(user=request.user)
    paginator = Paginator(documents, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST' and 'delete_document' in request.POST:
        document_id = request.POST.get('document_id')
        document = PkoDocument.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('pko_document')

    return render(request, 'pko_document_new.html', {'page_obj': page_obj})