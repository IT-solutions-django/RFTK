from django import forms
from invoice.models import AgreementDocument, InformationOrganization, BankDetailsOrganization, Buyer, BankDetailsBuyer, TemplateDocument


class AgreementDocumentForm(forms.ModelForm):
    # SAMPLE_CHOICES = [('', 'Выберите шаблон')] + [
    #     (obj.title, obj.title) for obj in TemplateDocument.objects.all()
    # ]

    sample = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        label='Шаблон',
        required=True
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
    bank_organization = forms.ModelChoiceField(
        queryset=BankDetailsOrganization.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк организации',
        label='Банк организации',
        required=False
    )
    counterparty = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Покупатель',
        label='Покупатель',
        required=True
    )
    bank_counterparty = forms.ModelChoiceField(
        queryset=BankDetailsBuyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк покупателя',
        label='Банк покупателя',
        required=False
    )

    class Meta:
        model = AgreementDocument
        fields = '__all__'
        exclude = ['user', 'dop_field']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        self.fields['sample'].choices = [('', 'Выберите шаблон')] + [
            (obj.title, obj.title) for obj in TemplateDocument.objects.all()
        ]

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)

            organization_id = request.POST.get("organization") or request.GET.get("organization") or (
                getattr(self.instance, "organization_id", None) if self.instance else None
            )
            if organization_id:
                self.fields['bank_organization'].queryset = BankDetailsOrganization.objects.filter(
                    organization_id=organization_id)

            counterparty_id = request.POST.get("counterparty") or request.GET.get("counterparty") or (
                getattr(self.instance, "counterparty_id", None) if self.instance else None
            )
            if counterparty_id:
                self.fields['bank_counterparty'].queryset = BankDetailsBuyer.objects.filter(
                    organization_id=counterparty_id)
