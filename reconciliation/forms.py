from django import forms
from invoice.models import ReconciliationDocument, ReconciliationDocumentTable, InformationOrganization, Buyer
from django.forms import modelformset_factory


class ReconciliationDocumentForm(forms.ModelForm):
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
        model = ReconciliationDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'period_from': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'period_by': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'balance_debit': forms.TextInput(attrs={'class': 'form-control'}),
            'balance_loan': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_act': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)


class ReconciliationDocumentTableForm(forms.ModelForm):
    class Meta:
        model = ReconciliationDocumentTable
        fields = '__all__'
        widgets = {
            'name_operation_org': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'style': 'height: 90px;'}),
            'debit_org': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'loan_org': forms.TextInput(attrs={'class': 'form-control'}),
            'name_operation_counterparty': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 90px;'}),
            'debit_counterparty': forms.TextInput(attrs={'class': 'form-control'}),
            'loan_counterparty': forms.TextInput(attrs={'class': 'form-control'}),
        }


ReconciliationDocumentTableFormSet = modelformset_factory(
    ReconciliationDocumentTable,
    form=ReconciliationDocumentTableForm,
    extra=1,
    max_num=1
)
