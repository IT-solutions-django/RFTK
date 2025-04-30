from django import forms
from invoice.models import CommercialOfferDocument, CommercialOfferDocumentTable, InformationOrganization, Buyer
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from datetime import date


class CommercialOfferDocumentForm(forms.ModelForm):
    NDS_CHOICES = [
        (-1, 'Без НДС'),
        (0, '0%'),
        (3, '3%'),
        (5, '5%'),
        (10, '10%'),
        (20, '20%')
    ]

    nds = forms.ChoiceField(
        choices=NDS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        label='НДС',
        required=False
    )

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
    is_stamp = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Добавить печать и подпись'
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

    class Meta:
        model = CommercialOfferDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%Y-%m-%d',attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),
            'naming': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_address', 'list': 'address_list'}),
        }
        labels = {
            'name': 'КП №',
            'date': 'Дата создания',
            'organization': 'Организация',
            'counterparty': 'Заказчик',
            'naming': 'Наименование',
            'address': 'Адрес'
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)


class CommercialOfferDocumentTableForm(forms.ModelForm):
    class Meta:
        model = CommercialOfferDocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'style': 'height: 90px;'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


CommercialOfferDocumentTableFormSet = modelformset_factory(
    CommercialOfferDocumentTable,
    form=CommercialOfferDocumentTableForm,
    extra=1,
    max_num=1
)
