from django import forms
from invoice.models import VatInvoiceDocument, InformationOrganization, Buyer


class VatInvoiceDocumentForm(forms.ModelForm):
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
    consignee = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Грузополучатель',
        label='Грузополучатель',
        required=True
    )
    shipper = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Грузоотправитель',
        label='Грузоотправитель',
        required=True
    )

    class Meta:
        model = VatInvoiceDocument
        fields = [
            'name',
            'date',
            'payment_document',
            'organization',
            'shipper',
            'counterparty',
            'consignee',
            'shipping_document',
            'state_ID_contract',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'shipping_document': forms.TextInput(
                attrs={'class': 'form-control'}),
            'state_ID_contract': forms.TextInput(
                attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_document': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название документа',
            'date': 'Дата создания документа',
            'organization': 'Организация',
            'shipper': 'Грузоотправитель',
            'counterparty': 'Контрагент',
            'consignee': 'Грузополучатель',
            'shipping_document': 'Документ об отгрузке',
            'state_ID_contract': 'Идентификатор гос. контракта',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['consignee'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['shipper'].queryset = Buyer.objects.filter(user=request.user)
