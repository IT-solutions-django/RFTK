from django import forms
from invoice.models import PackingListDocument, PackingListDocumentTable, InformationOrganization, Buyer, \
    BankDetailsBuyer
from django.forms import modelformset_factory
from invoice.models import BankDetailsOrganization


class PackingListDocumentForm(forms.ModelForm):
    bank_organization = forms.ModelChoiceField(
        queryset=BankDetailsOrganization.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк организации',
        label='Банк организации',
        required=True
    )
    bank_counterparty = forms.ModelChoiceField(
        queryset=BankDetailsBuyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк контрагента',
        label='Банк контрагента',
        required=True
    )
    organization = forms.ModelChoiceField(
        queryset=InformationOrganization.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Организация',
        label='Организация',
        required=True
    )
    counterparty = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Контрагент',
        label='Контрагент',
        required=True
    )
    consignee = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Грузополучатель',
        label='Грузополучатель',
        required=True
    )
    shipper = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Грузоотправитель',
        label='Грузоотправитель',
        required=True
    )

    class Meta:
        model = PackingListDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bank_counterparty': forms.Select(attrs={'class': 'form-select select2'}),
            'structural_division': forms.TextInput(attrs={'class': 'form-control'}),
            'base': forms.TextInput(attrs={'class': 'form-control'}),
            'number_base': forms.TextInput(attrs={'class': 'form-control'}),
            'date_base': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'packing_list': forms.TextInput(attrs={'class': 'form-control'}),
            'date_packing_list': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'shipping_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_receipt': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Название',
            'date': 'Дата создания',
            'organization': 'Организация',
            'bank_organization': 'Банк организации',
            'shipper': 'Грузоотправитель',
            'counterparty': 'Контрагент',
            'bank_counterparty': 'Банк контрагента',
            'consignee': 'Грузополучатель',
            'structural_division': 'Структурное подразделение',
            'base': 'Основание',
            'number_base': 'Номер основания',
            'date_base': 'Дата основания',
            'packing_list': 'Транспортная накладная',
            'date_packing_list': 'Дата накладной',
            'shipping_date': 'Дата отгрузки',
            'date_of_receipt': 'Дата получения',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['consignee'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['shipper'].queryset = Buyer.objects.filter(user=request.user)

            organization_id = request.POST.get("organization") or request.GET.get("organization")
            if organization_id:
                self.fields['bank_organization'].queryset = BankDetailsOrganization.objects.filter(
                    organization_id=organization_id)

            counterparty_id = request.POST.get("counterparty") or request.GET.get("counterparty")
            if counterparty_id:
                self.fields['bank_counterparty'].queryset = BankDetailsBuyer.objects.filter(
                    organization_id=counterparty_id)


class PackingListDocumentTableForm(forms.ModelForm):
    class Meta:
        model = PackingListDocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'type_of_packaging': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'gross_weight': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'net_weight': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


PackingListDocumentTableFormSet = modelformset_factory(
    PackingListDocumentTable,
    form=PackingListDocumentTableForm,
    extra=1
)
