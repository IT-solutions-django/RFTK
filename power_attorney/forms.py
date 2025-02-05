from django import forms
from invoice.models import PowerAttorneyDocument, PowerAttorneyDocumentTable, InformationOrganization, Buyer, \
    BankDetailsBuyer
from django.forms import modelformset_factory
from invoice.models import BankDetailsOrganization


class PowerAttorneyDocumentForm(forms.ModelForm):
    bank_organization = forms.ModelChoiceField(
        queryset=BankDetailsOrganization.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк организации',
        label='Банк организации',
        required=True
    )
    organization = forms.ModelChoiceField(
        queryset=InformationOrganization.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Организация',
        label='Организация',
        required=True
    )

    class Meta:
        model = PowerAttorneyDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'validity_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_issue': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_receive_from': forms.TextInput(attrs={'class': 'form-control'}),
            'according_document': forms.TextInput(attrs={'class': 'form-control'}),
            'person_power': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_series': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'issued_by': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)

            organization_id = request.POST.get("organization") or request.GET.get("organization")
            if organization_id:
                self.fields['bank_organization'].queryset = BankDetailsOrganization.objects.filter(
                    organization_id=organization_id)


class PowerAttorneyDocumentTableForm(forms.ModelForm):
    class Meta:
        model = PowerAttorneyDocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


PowerAttorneyDocumentTableFormSet = modelformset_factory(
    PowerAttorneyDocumentTable,
    form=PowerAttorneyDocumentTableForm,
    extra=1
)
