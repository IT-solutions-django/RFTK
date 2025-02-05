from django import forms
from invoice.models import CommercialOfferDocument, CommercialOfferDocumentTable, InformationOrganization, Buyer
from django.forms import modelformset_factory


class CommercialOfferDocumentForm(forms.ModelForm):
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
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


CommercialOfferDocumentTableFormSet = modelformset_factory(
    CommercialOfferDocumentTable,
    form=CommercialOfferDocumentTableForm,
    extra=1
)
