from django import forms
from invoice.models import SalesReceiptDocument, SalesReceiptDocumentTable, InformationOrganization, Buyer
from django.forms import modelformset_factory
from datetime import date


class SalesReceiptDocumentForm(forms.ModelForm):
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

    class Meta:
        model = SalesReceiptDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),

        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)


class SalesReceiptDocumentTableForm(forms.ModelForm):
    class Meta:
        model = SalesReceiptDocumentTable
        fields = '__all__'
        widgets = {
            'article_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'style': 'height: 90px;'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


SalesReceiptDocumentTableFormSet = modelformset_factory(
    SalesReceiptDocumentTable,
    form=SalesReceiptDocumentTableForm,
    extra=1,
    max_num=1
)
