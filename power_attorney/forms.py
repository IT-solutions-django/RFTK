from django import forms
from invoice.models import PowerAttorneyDocument, PowerAttorneyDocumentTable, InformationOrganization, Buyer, \
    BankDetailsBuyer
from django.forms import modelformset_factory
from invoice.models import BankDetailsOrganization
from datetime import date


class PowerAttorneyDocumentForm(forms.ModelForm):
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
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),
            'validity_period': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'date_issue': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
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

            organization_id = request.POST.get("organization") or request.GET.get("organization") or (
                getattr(self.instance, "organization_id", None) if self.instance else None
            )
            if organization_id:
                self.fields['bank_organization'].queryset = BankDetailsOrganization.objects.filter(
                    organization_id=organization_id)


class PowerAttorneyDocumentTableForm(forms.ModelForm):
    class Meta:
        model = PowerAttorneyDocumentTable
        fields = '__all__'
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'style': 'height: 90px;'}),
            'unit_of_measurement': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
        }


PowerAttorneyDocumentTableFormSet = modelformset_factory(
    PowerAttorneyDocumentTable,
    form=PowerAttorneyDocumentTableForm,
    extra=1,
    max_num=1
)


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
