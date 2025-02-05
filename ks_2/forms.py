from django import forms
from invoice.models import Ks2Document, Ks2DocumentTable, InformationOrganization, Buyer
from django.forms import modelformset_factory


class Ks2DocumentForm(forms.ModelForm):
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
        required=True
    )

    class Meta:
        model = Ks2Document
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_construction': forms.TextInput(attrs={'class': 'form-control'}),
            'address_construction': forms.TextInput(attrs={'class': 'form-control'}),
            'name_object': forms.TextInput(attrs={'class': 'form-control'}),
            'view_okdp': forms.TextInput(attrs={'class': 'form-control'}),
            'number_agreement': forms.TextInput(attrs={'class': 'form-control'}),
            'price_outlay': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_by': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_agreement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['investor'].queryset = Buyer.objects.filter(user=request.user)


class Ks2DocumentTableForm(forms.ModelForm):
    class Meta:
        model = Ks2DocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'number_outlay': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'number_unit': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


Ks2DocumentTableFormSet = modelformset_factory(
    Ks2DocumentTable,
    form=Ks2DocumentTableForm,
    extra=1
)
