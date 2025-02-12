from django import forms
from invoice.models import RkoDocument, InformationOrganization


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
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'payer': forms.TextInput(attrs={'class': 'form-control'}),
            'passport': forms.TextInput(attrs={'class': 'form-control'}),
            'account_debit': forms.TextInput(attrs={'class': 'form-control'}),
            'account_loan': forms.TextInput(attrs={'class': 'form-control'}),
            'summa': forms.TextInput(attrs={'class': 'form-control'}),
            'base': forms.TextInput(attrs={'class': 'form-control'}),
            'annex': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
