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


class BankOrganizationForm(forms.ModelForm):
    class Meta:
        model = BankDetailsOrganization
        fields = '__all__'
        exclude = ['organization']

        widgets = {
            'bic': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите БИК банка', 'pattern': '[0-9]+',
                       'title': 'БИК может содержать только цифры'}),
            'naming': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название банка'}),
            'location': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'list': 'address_list_bank'}),
            'correspondent_account': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите кор.счет', 'pattern': '[0-9]+',
                       'title': 'Кор.счет может содержать только цифры'}),
            'current_account': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите расчетный счет', 'pattern': '[0-9]+',
                       'title': 'Расчетный счет может содержать только цифры'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
            field.required = False

    def clean(self):
        cleaned_data = super().clean()

        if any(cleaned_data.values()):
            required_fields = ['bic', 'naming', 'location', 'correspondent_account', 'current_account']
            missing_fields = [field for field in required_fields if not cleaned_data.get(field)]

            if missing_fields:
                raise forms.ValidationError("Все поля банковских данных обязательны, если хотя бы одно заполнено.")

        return cleaned_data


class BankCounForm(forms.ModelForm):
    class Meta:
        model = BankDetailsBuyer
        fields = '__all__'
        exclude = ['organization']

        widgets = {
            'bic': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите БИК банка', 'pattern': '[0-9]+',
                       'title': 'БИК может содержать только цифры'}),
            'naming': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название банка'}),
            'location': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'list': 'address_list_bank'}),
            'correspondent_account': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите кор.счет', 'pattern': '[0-9]+',
                       'title': 'Кор.счет может содержать только цифры'}),
            'current_account': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите расчетный счет', 'pattern': '[0-9]+',
                       'title': 'Расчетный счет может содержать только цифры'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''
            field.required = False

    def clean(self):
        cleaned_data = super().clean()

        if any(cleaned_data.values()):
            required_fields = ['bic', 'naming', 'location', 'correspondent_account', 'current_account']
            missing_fields = [field for field in required_fields if not cleaned_data.get(field)]

            if missing_fields:
                raise forms.ValidationError("Все поля банковских данных обязательны, если хотя бы одно заполнено.")

        return cleaned_data