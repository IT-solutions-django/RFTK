from django import forms
from .models import (InvoiceDocument, InformationOrganization, BankDetailsOrganization, Buyer,
                     BankDetailsBuyer, InvoiceDocumentTable)
from django.forms import modelformset_factory


class InvoiceDocumentForm(forms.ModelForm):
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

    CURRENCY_CHOICES = [
        ('Российский рубль, 643', 'Российский рубль, 643'),
        ('Доллар США, 840', 'Доллар США, 840'),
        ('Евро, 978', 'Евро, 978')
    ]

    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        label='Валюта',
        required=False
    )
    is_stamp = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Добавить печать и подпись'
    )
    bank_organization = forms.ModelChoiceField(
        queryset=BankDetailsOrganization.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк организации',
        label='Банк организации',
        required=False
    )
    bank_counterparty = forms.ModelChoiceField(
        queryset=BankDetailsBuyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Банк контрагента',
        label='Банк контрагента',
        required=False
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
    consignee = forms.ModelChoiceField(
        queryset=Buyer.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select select2'}),
        empty_label='Грузополучатель',
        label='Грузополучатель',
        required=False
    )

    class Meta:
        model = InvoiceDocument
        fields = [
            'name',
            'date',
            'organization',
            'bank_organization',
            'counterparty',
            'bank_counterparty',
            'consignee',
            'purpose_of_payment',
            'payment_for',
            'agreement',
            'currency',
            'nds',
            'is_stamp'
        ]
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'purpose_of_payment': forms.TextInput(
                attrs={'placeholder': 'Например, Авансовый платёж', 'class': 'form-control'}),
            'payment_for': forms.TextInput(
                attrs={'placeholder': 'Опишите, за что производится оплата', 'class': 'form-control'}),
            'agreement': forms.TextInput(attrs={'placeholder': 'Номер и дата договора', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Счет на оплату №',
            'date': 'Дата создания документа',
            'organization': 'Организация',
            'counterparty': 'Контрагент',
            'bank_counterparty': 'Банк контрагента',
            'consignee': 'Грузополучатель',
            'purpose_of_payment': 'Назначение платежа',
            'payment_for': 'Оплата за',
            'agreement': 'Договор',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
            self.fields['consignee'].queryset = Buyer.objects.filter(user=request.user)

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


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = InformationOrganization
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'naming': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название организации'}),
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ИНН', 'pattern': '[0-9]+',
                                          'title': 'ИНН может содержать только цифры'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите КПП', 'pattern': '[0-9]+',
                                          'title': 'КПП может содержать только цифры'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9]+',
                                           'title': 'ОГРН может содержать только цифры', 'placeholder': 'ОГРН/ОГРНИП'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'list': 'address_list'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона', 'inputmode': 'tel',
                       'type': 'tel'}),
            'fax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер факса'}),
            'position_at_work': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите должность'}),
            'supervisor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя руководителя'}),
            'accountant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя бухгалтера'}),
            'code_company': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите условное наимнование организации'}),
            'stamp': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'signature': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'stamp':
                field.label = ''
                field.help_text = 'Загрузите печать компании'
            elif name == 'signature':
                field.label = ''
                field.help_text = 'Загрузите подпись руководителя'
            else:
                field.help_text = ''


class BankDetailsOrganizationForm(forms.ModelForm):
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


class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'naming': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название организации'}),
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ИНН', 'pattern': '[0-9]+',
                                          'title': 'ИНН может содержать только цифры'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите КПП', 'pattern': '[0-9]+',
                                          'title': 'КПП может содержать только цифры'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ОГРН', 'pattern': '[0-9]+',
                                           'title': 'ОГРН может содержать только цифры'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите адрес', 'list': 'address_list'}),
            'phone': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите телефон', 'inputmode': 'tel', 'type': 'tel'}),
            'code_company': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Введите условное наимнование организации'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ''


class BankCounterpartyForm(forms.ModelForm):
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


class InvoiceDocumentTableForm(forms.ModelForm):
    class Meta:
        model = InvoiceDocumentTable
        fields = [
            'name',
            'unit_of_measurement',
            'quantity',
            'price',
            'amount',
            'discount',
        ]
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', "style": "height: 90px"}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
        }


InvoiceDocumentTableFormSet = modelformset_factory(
    InvoiceDocumentTable,
    form=InvoiceDocumentTableForm,
    extra=1,
    max_num=1
)
