from django import forms
from invoice.models import OutlayDocument, InformationOrganization, Buyer
from datetime import date


class OutlayDocumentForm(forms.ModelForm):
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
        model = OutlayDocument
        fields = '__all__'
        exclude = ['table_product', 'user']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number_outlay': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control w-md-25', 'type': 'date', 'value': date.today().strftime('%Y-%m-%d')}),
            'base': forms.TextInput(attrs={'class': 'form-control'}),
            'work_time': forms.TextInput(attrs={'class': 'form-control'}),
            'name_construction': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_address', 'list': 'address_list'}),
        }
        labels = {
            'name': 'Название документа',
            'number_outlay': 'Смета №',
            'date': 'Дата создания',
            'organization': 'Организация',
            'counterparty': 'Заказчик',
            'base': 'Основание',
            'address': 'По адресу',
            'work_time': 'Срок выполнения работ',
            'name_construction': 'Наименование стройки',
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if request:
            self.fields['organization'].queryset = InformationOrganization.objects.filter(user=request.user)
            self.fields['counterparty'].queryset = Buyer.objects.filter(user=request.user)
