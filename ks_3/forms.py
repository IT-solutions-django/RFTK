from django import forms
from invoice.models import Ks3Document, Ks3DocumentTable, InformationOrganization, Buyer
from django.forms import modelformset_factory
from datetime import date


class Ks3DocumentForm(forms.ModelForm):
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
    investor = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Инвестор',
        label='Инвестор',
        required=False
    )

    class Meta:
        model = Ks3Document
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'name_construction': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'address_construction': forms.TextInput(
                attrs={'class': 'form-control w-md-50', 'id': 'id_address', 'list': 'address_list'}),
            'number_agreement': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),
            'period_by': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date'}),
            'period_from': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date'}),
            'date_agreement': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['investor'].queryset = Buyer.objects.filter(user=request.user)


class Ks3DocumentTableForm(forms.ModelForm):
    class Meta:
        model = Ks3DocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'style': 'height: 90px;'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price_from_construction': forms.NumberInput(attrs={'class': 'form-control'}),
            'price_from_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


Ks3DocumentTableFormSet = modelformset_factory(
    Ks3DocumentTable,
    form=Ks3DocumentTableForm,
    extra=1,
    max_num=1
)
