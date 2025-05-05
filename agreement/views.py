from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from invoice.models import AgreementDocument, TemplateDocument, ValueLabel, InformationOrganization, Buyer
from .forms import AgreementDocumentForm, BankOrganizationForm, BankCounForm
from django.urls import reverse_lazy
from invoice.forms import OrganizationForm, BankDetailsOrganizationForm, CounterpartyForm, BankCounterpartyForm
from agreement.utils.excel import create_agreement_excel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.template.loader import render_to_string
from agreement.utils.agreement_registry_pdf import create_agreement_registry_pdf


class AgreementDocumentCreateView(LoginRequiredMixin, CreateView):
    model = AgreementDocument
    form_class = AgreementDocumentForm
    template_name = 'agreement_document_form_new.html'
    success_url = reverse_lazy('agreement_document')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['org_form'] = OrganizationForm(prefix='organization')
        context['bank_form'] = BankDetailsOrganizationForm(prefix='bank')
        context['counterparty_form'] = CounterpartyForm(prefix='counterparty')
        context['bank_org'] = BankOrganizationForm(prefix='bank_org')
        context['bank_coun'] = BankCounForm(prefix='bank_coun')
        context['counterparty_bank_form'] = BankCounterpartyForm(prefix='counterparty_bank')

        return context

    def form_valid(self, form):
        template_name = form.cleaned_data.get('sample')
        template_sample = TemplateDocument.objects.filter(title=template_name).first()
        labels = template_sample.labels.all()

        list_value_dop_field = []

        for label in labels:
            label_code = self.request.POST.get(f'{label.label_code}')
            if label_code:
                value_label = ValueLabel(label=label, value=label_code)
                value_label.save()
                list_value_dop_field.append(value_label)

        document_name = form.cleaned_data.get('name')
        document_date = form.cleaned_data.get('date')
        existing_document = AgreementDocument.objects.filter(name=document_name, date=document_date)
        if existing_document:
            self.object = form.save(commit=False)
            self.object.pk = existing_document.first().pk
            self.object.user = self.request.user
            self.object.save()
            self.object.dop_field.add(*list_value_dop_field)
        else:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            self.object.dop_field.add(*list_value_dop_field)

        context = {
            'title': template_sample.title,
            'content': template_sample.content
        }

        # context = form.cleaned_data
        #
        html_string = render_to_string('supply_contract.html', context)

        dop_fields = self.object.dop_field.all()

        for label in labels:
            value_label = dop_fields.filter(label=label).first()
            if value_label:
                html_string = html_string.replace(label.label_code, value_label.value)

        for label in labels:
            if label.label_code == '{date_doc}':
                html_string = html_string.replace(label.label_code, str(form.cleaned_data['date']))
            elif label.label_code == '{number_doc}':
                html_string = html_string.replace(label.label_code, form.cleaned_data['name'])
            elif label.label_code == '{name}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].naming)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{address}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].address)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{inn}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].inn)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{kpp}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].kpp)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{ogrn}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].ogrn)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{phone}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].phone)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_schet}':
                if form.cleaned_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_organization'].namimg)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_bik}':
                if form.cleaned_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_organization'].bic)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_korr}':
                if form.cleaned_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_organization'].correspondent_account)
                else:
                    html_string = html_string.replace(label.label_code,
                                                      '')
            elif label.label_code == '{org_caption_director}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].position_at_work)
                else:
                    html_string = html_string.replace(label.label_code,
                                                      '')
            elif label.label_code == '{org_director}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].supervisor)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{org_buh}':
                if form.cleaned_data['organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['organization'].accountant)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{bank_address}':
                if form.cleaned_data['bank_organization']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_organization'].location)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_name}':
                if form.cleaned_data['counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['counterparty'].naming)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_inn}':
                if form.cleaned_data['counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['counterparty'].inn)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_kpp}':
                if form.cleaned_data['counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['counterparty'].kpp)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_ogrn}':
                if form.cleaned_data['counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['counterparty'].ogrn)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_address}':
                if form.cleaned_data['counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['counterparty'].address)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_phone}':
                if form.cleaned_data['counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['counterparty'].phone)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_bank_name}':
                if form.cleaned_data['bank_counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_counterparty'].naming)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_bank_bic}':
                if form.cleaned_data['bank_counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_counterparty'].bic)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_bank_address}':
                if form.cleaned_data['bank_counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_counterparty'].location)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_bank_schet}':
                if form.cleaned_data['bank_counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_counterparty'].current_account)
                else:
                    html_string = html_string.replace(label.label_code, '')
            elif label.label_code == '{partner_bank_korr}':
                if form.cleaned_data['bank_counterparty']:
                    html_string = html_string.replace(label.label_code, form.cleaned_data['bank_counterparty'].correspondent_account)
                else:
                    html_string = html_string.replace(label.label_code, '')

        organization = form.cleaned_data['organization']
        is_stamp = form.cleaned_data['is_stamp']

        if self.request.POST.get("download_pdf") == "true":
            response = create_agreement_excel(html_string, organization, is_stamp, True)
            return response

        response = create_agreement_excel(html_string, organization, is_stamp)
        return response


def agreement_document(request):
    query = request.GET.get('q', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    org_param = request.GET.get('filter_org', '')
    coun_param = request.GET.get('filter_coun', '')
    sort_param = request.GET.get('sort', '')

    documents = AgreementDocument.objects.select_related('organization', 'counterparty').filter(user=request.user)

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
        document = AgreementDocument.objects.get(id=document_id, user=request.user)
        document.delete()
        return redirect('agreement_document')

    organizations = InformationOrganization.objects.filter(user=request.user)

    counterparty = Buyer.objects.filter(user=request.user)

    return render(request, 'agreement_document_new.html',
                  {'page_obj': page_obj, 'query': query, 'date_from': date_from, 'date_to': date_to, 'current_page': page_obj.number, 'total_pages': paginator.num_pages, 'organizations': organizations, 'counterparty':  counterparty, 'page_range': page_range})


def agreement_registry(request):
    utd_documents_all = AgreementDocument.objects.select_related('organization', 'counterparty').filter(user=request.user)

    context = {
        'utd_documents_all': utd_documents_all
    }

    html_string = render_to_string('agreement_registry.html', context)

    response = create_agreement_registry_pdf(html_string)

    return response
