from django import forms
from invoice.models import RkoDocument, InformationOrganization
from datetime import date


class RkoDocumentForm(forms.ModelForm):
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
        model = RkoDocument
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'payer': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'passport': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'account_debit': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'account_loan': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'summa': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'base': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'annex': forms.TextInput(attrs={'class': 'form-control w-md-50'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
