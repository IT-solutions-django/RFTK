from django import forms
from invoice.models import UtdDocumentTable, UtdDocument, InformationOrganization, Buyer
from django.forms import modelformset_factory


class UtdDocumentForm(forms.ModelForm):
    CURRENCY_CHOICES = [
        ('Российский рубль, 643', 'Российский рубль, 643'),
        ('Доллар США, 840', 'Доллар США, 840'),
        ('Евро, 978', 'Евро, 978')
    ]

    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        label='Валюта',
        required=False
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
    is_stamp = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Добавить печать и подпись'
    )

    class Meta:
        model = UtdDocument
        fields = [
            'name',
            'date',
            'payment_document',
            'organization',
            'shipper',
            'counterparty',
            'consignee',
            'shipping_document',
            'state_ID_contract',
            'basis_for_transfer',
            'data_transportation',
            'shipment_date',
            'date_of_receipt',
            'type_document',
            'currency',
            'nds',
            'is_stamp'
        ]
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'shipment_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_receipt': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'shipping_document': forms.TextInput(
                attrs={'class': 'form-control'}),
            'state_ID_contract': forms.TextInput(
                attrs={'class': 'form-control'}),
            'basis_for_transfer': forms.TextInput(attrs={'class': 'form-control'}),
            'data_transportation': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_document': forms.TextInput(attrs={'class': 'form-control'}),
            'type_document': forms.TextInput(attrs={'class': 'form-control'}),
            'nds': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'УПД №',
            'date': 'Дата создания документа',
            'organization': 'Организация',
            'shipper': 'Грузоотправитель',
            'counterparty': 'Контрагент',
            'consignee': 'Грузополучатель',
            'shipping_document': 'Документ об отгрузке',
            'state_ID_contract': 'Идентификатор гос. контракта',
            'basis_for_transfer': 'Основание передачи',
            'data_transportation': 'Данные о транспортировке и грузе',
            'shipment_date': 'Дата отгрузки',
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


class UtdDocumentTableForm(forms.ModelForm):
    class Meta:
        model = UtdDocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'product_code': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'product_type_code': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'excise': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'number_GTD': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


UtdDocumentTableFormSet = modelformset_factory(
    UtdDocumentTable,
    form=UtdDocumentTableForm,
    extra=1
)
