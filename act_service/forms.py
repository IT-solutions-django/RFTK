from django import forms
from invoice.models import ActServiceDocument, InformationOrganization, Buyer
from datetime import date


class ActServiceDocumentForm(forms.ModelForm):
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
        model = ActServiceDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),
            'payment_for': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'agreement': forms.TextInput(attrs={'class': 'form-control w-md-50'}),

        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
