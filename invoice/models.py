from django.db import models
from user.models import CustomUser
from django.core.exceptions import ValidationError
import re


def validate_inn(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('ИНН должен содержать только цифры.')


def validate_kpp(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('КПП должен содержать только цифры.')


def validate_ogrn(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('ОГРН должен содержать только цифры.')


def validate_phone(value):
    pattern = r'^\+7\d{10}$'
    if not re.fullmatch(pattern, value):
        raise ValidationError('Введите корректный номер в формате +7XXXXXXXXXX.')


def validate_nds(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('НДС должен содержать только цифры.')


def validate_bic(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('БИК должен содержать только цифры.')


def validate_correspondent_account(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('Корреспондентский счёт должен содержать только цифры.')


def validate_current_account(value):
    if not re.fullmatch(r'\d+', value):
        raise ValidationError('Расчетный счёт должен содержать только цифры.')


class InformationOrganization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    naming = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование организации')
    inn = models.CharField(max_length=50, verbose_name='ИНН', help_text='Введите ИНН организации',
                           validators=[validate_inn])
    kpp = models.CharField(max_length=50, verbose_name='КПП', help_text='Для ООО',
                           validators=[validate_kpp], null=True, blank=True)
    ogrn = models.CharField(max_length=50, verbose_name='ОГРН/ОГРНИП', help_text='Введите ОГРН организации',
                            validators=[validate_ogrn], blank=True, null=True)
    address = models.TextField(verbose_name='Адрес', help_text='Введите адрес организации', null=True, blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', help_text='Введите телефон организации', null=True,
                             blank=True)
    fax = models.CharField(max_length=50, verbose_name='Факс', help_text='Введите факс организации', null=True,
                           blank=True)
    position_at_work = models.CharField(max_length=50, verbose_name='Должность руководителя',
                                        help_text='Введите должность руководителя организации', null=True, blank=True)
    supervisor = models.CharField(max_length=100, verbose_name='Руководитель',
                                  help_text='Введите ФИО руководителя организации', null=True, blank=True)
    accountant = models.CharField(max_length=100, verbose_name='Бухгалтер',
                                  help_text='Введите ФИО бухгалтера организации', null=True, blank=True)
    code_company = models.CharField(max_length=50, verbose_name='Условное наименование организации',
                                    help_text='Пример: Поставщик, Исполнитель, Продавец', null=True, blank=True)
    stamp = models.ImageField(upload_to='stamps', blank=True, null=False, verbose_name='Печать',
                              help_text='Добавьте печать')
    signature = models.ImageField(upload_to='signatures', blank=True, null=True, verbose_name='Подпись',
                                  help_text='Добавьте подпись')

    class Meta:
        verbose_name = "Информация об организации"
        verbose_name_plural = "Информация об организации"

    def __str__(self):
        return self.naming


class BankDetailsOrganization(models.Model):
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация',
                                     help_text='Выберите организацию')
    bic = models.CharField(max_length=100, verbose_name='БИК', help_text='Введите БИК банка', validators=[validate_bic])
    naming = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование банка')
    location = models.TextField(verbose_name='Местонахождение', help_text='Введите местонахождение банка')
    correspondent_account = models.CharField(max_length=100, verbose_name='Корреспондентский счёт',
                                             help_text='Введите № корреспондентского счёта банка',
                                             validators=[validate_correspondent_account])
    current_account = models.CharField(max_length=100, verbose_name='Расчетный счёт',
                                       help_text='Введите № расчетного счёта банка',
                                       validators=[validate_current_account])

    class Meta:
        verbose_name = "Банк организации"
        verbose_name_plural = "Банк организации"

    def __str__(self):
        return f'Банк: {self.naming}. Организация: {self.organization.naming}'


class Buyer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    naming = models.CharField(max_length=100, verbose_name='Наименование',
                              help_text='Введите наименование организации покупателя')
    inn = models.CharField(max_length=50, verbose_name='ИНН', help_text='Введите ИНН организации покупателя',
                           validators=[validate_inn])
    kpp = models.CharField(max_length=50, verbose_name='КПП', help_text='Введите КПП организации покупателя',
                           validators=[validate_kpp], null=True, blank=True)
    ogrn = models.CharField(max_length=50, verbose_name='ОГРН/ОГРНИП', help_text='Введите ОГРН организации покупателя',
                            validators=[validate_ogrn], null=True, blank=True)
    address = models.TextField(verbose_name='Адрес', help_text='Введите адрес организации покупателя', null=True,
                               blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', help_text='Введите телефон организации покупателя',
                             null=True, blank=True)
    code_company = models.CharField(max_length=50, verbose_name='Условное наименование организации покупателя',
                                    help_text='Пример: Клиент, Заказчик, Покупатель', null=True, blank=True)

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагент"

    def __str__(self):
        return self.naming


class BankDetailsBuyer(models.Model):
    organization = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Организация покупателя',
                                     help_text='Выберите организацию покупателя')
    bic = models.CharField(max_length=100, verbose_name='БИК', help_text='Введите БИК банка', validators=[validate_bic])
    naming = models.CharField(max_length=100, verbose_name='Наименование', help_text='Введите наименование банка')
    location = models.TextField(verbose_name='Местонахождение', help_text='Введите местонахождение банка')
    correspondent_account = models.CharField(max_length=100, verbose_name='Корреспондентский счёт',
                                             help_text='Введите № корреспондентского счёта банка',
                                             validators=[validate_correspondent_account])
    current_account = models.CharField(max_length=100, verbose_name='Расчетный счёт',
                                       help_text='Введите № расчетного счёта банка',
                                       validators=[validate_current_account])

    class Meta:
        verbose_name = "Банк контрагента"
        verbose_name_plural = "Банк контрагента"

    def __str__(self):
        return f'Банк: {self.naming}. Организация покупателя: {self.organization.naming}'


class InvoiceDocumentTable(models.Model):
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    discount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Скидка',
                                   help_text='Введите скидку на товар', null=True, blank=True)

    class Meta:
        verbose_name = "Таблица для документа счет"
        verbose_name_plural = "Таблица для документа счет"

    def __str__(self):
        return self.name


class UtdDocumentTable(models.Model):
    product_code = models.CharField(max_length=50, verbose_name='Код товара', help_text='Введите код товара / услуг',
                                    null=True, blank=True)
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    product_type_code = models.CharField(max_length=50, verbose_name='Код вида товара',
                                         help_text='Введите код вида товара', null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    excise = models.CharField(max_length=50, verbose_name='Акциз', help_text='Введите акциз', null=True, blank=True)
    quantity = models.FloatField(verbose_name='Количество', help_text='Введите количество товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')
    country = models.CharField(max_length=50, verbose_name='Страна', help_text='Введите страну', null=True, blank=True)
    number_GTD = models.TextField(verbose_name='№ ГТД', help_text='Введите № ГТД', null=True, blank=True)

    class Meta:
        verbose_name = "Таблица для документа упд"
        verbose_name_plural = "Таблица для документа упд"

    def __str__(self):
        return self.name


class InvoiceDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Счет на оплату №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    bank_organization = models.ForeignKey(BankDetailsOrganization, on_delete=models.CASCADE,
                                          verbose_name='Банк организации', help_text='Выберите банк организации',
                                          null=True, blank=True)
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty')
    bank_counterparty = models.ForeignKey(BankDetailsBuyer, on_delete=models.CASCADE, verbose_name='Банк контрагента',
                                          null=True, blank=True)
    consignee = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Грузополучатель',
                                  related_name='as_consignee', null=True, blank=True)
    purpose_of_payment = models.CharField(max_length=150, verbose_name='Назначение платежа', null=True, blank=True)
    payment_for = models.CharField(max_length=150, verbose_name='Оплата за', null=True, blank=True)
    agreement = models.CharField(max_length=150, verbose_name='Договор', null=True, blank=True)
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(InvoiceDocumentTable, verbose_name='Таблица товаров', blank=True)

    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счет"

    def __str__(self):
        return f'{self.name} от {self.date}'


class UtdDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.TextField(verbose_name='Название')
    date = models.DateField(verbose_name='Дата создания')
    payment_document = models.CharField(max_length=500, verbose_name='К платежно-расчетному документу', null=True,
                                        blank=True)
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    shipper = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Грузоотправитель',
                                related_name='as_shipper_utd', null=True, blank=True)
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_utd')
    consignee = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Грузополучатель',
                                  related_name='as_consignee_utd', null=True, blank=True)
    shipping_document = models.CharField(max_length=500, verbose_name='Документ об отгрузке', null=True, blank=True)
    state_ID_contract = models.CharField(max_length=150, verbose_name='Идентификатор гос. контракта', null=True,
                                         blank=True)
    table_product = models.ManyToManyField(UtdDocumentTable, verbose_name='Таблица товаров')
    basis_for_transfer = models.CharField(max_length=150, verbose_name='Основание передачи', null=True, blank=True)
    data_transportation = models.CharField(max_length=150, verbose_name='Данные о транспортировке и грузе', null=True,
                                           blank=True)
    shipment_date = models.DateField(verbose_name='Дата отгрузки', null=True, blank=True)
    date_of_receipt = models.DateField(verbose_name='Дата получения', null=True, blank=True)
    type_document = models.CharField(max_length=150, verbose_name='Тип документа', blank=True, null=True,
                                     default='Передаточный документ(акт)')
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=-1)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)

    class Meta:
        verbose_name = "Упд"
        verbose_name_plural = "Упд"

    def __str__(self):
        return f'{self.name} от {self.date}'


class VatInvoiceDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Название')
    date = models.DateField(verbose_name='Дата создания')
    payment_document = models.CharField(max_length=500, verbose_name='К платежно-расчетному документу', null=True,
                                        blank=True)
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    shipper = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Грузоотправитель',
                                related_name='as_shipper_vat', null=True, blank=True)
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_vat')
    consignee = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Грузополучатель',
                                  related_name='as_consignee_vat', null=True, blank=True)
    shipping_document = models.CharField(max_length=500, verbose_name='Документ об отгрузке', null=True, blank=True)
    state_ID_contract = models.CharField(max_length=150, verbose_name='Идентификатор гос. контракта', null=True,
                                         blank=True)
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(UtdDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Счет-фактура"
        verbose_name_plural = "Счет-фактура"

    def __str__(self):
        return f'{self.name} от {self.date}'


class PackingListDocumentTable(models.Model):
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    product_code = models.CharField(max_length=50, verbose_name='Код товара', help_text='Введите код товара')
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    type_of_packaging = models.CharField(max_length=100, verbose_name='Вид упаковки', help_text='Введите вид упаковки')
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')
    gross_weight = models.IntegerField(verbose_name='Масса брутто', help_text='Введите масса брутто')
    net_weight = models.IntegerField(verbose_name='Масса нетто', help_text='Введите масса нетто')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')

    class Meta:
        verbose_name = "Таблица для документа товарная накладная"
        verbose_name_plural = "Таблица для документа товарная накладная"

    def __str__(self):
        return self.name


class PackingListDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Название')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    bank_organization = models.ForeignKey(BankDetailsOrganization, on_delete=models.CASCADE,
                                          verbose_name='Банк организации', help_text='Выберите банк организации'
                                          )
    shipper = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Грузоотправитель',
                                related_name='as_shipper_packing')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_packing')
    bank_counterparty = models.ForeignKey(BankDetailsBuyer, on_delete=models.CASCADE, verbose_name='Банк контрагента')
    consignee = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Грузополучатель',
                                  related_name='as_consignee_packing')
    structural_division = models.CharField(max_length=500, verbose_name='Структурное подразделение')
    base = models.CharField(max_length=500, verbose_name='Основание')
    number_base = models.CharField(max_length=100, verbose_name='Номер основания')
    date_base = models.DateField(verbose_name='Дата основания')
    packing_list = models.CharField(max_length=250, verbose_name='Транспортная накладная')
    date_packing_list = models.DateField(verbose_name='Дата')
    shipping_date = models.DateField(verbose_name='Дата отгрузки')
    date_of_receipt = models.DateField(verbose_name='Дата получения')
    table_product = models.ManyToManyField(PackingListDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Товарная накладная"
        verbose_name_plural = "Товарная накладная"

    def __str__(self):
        return f'{self.name} от {self.date}'


class CommercialOfferDocumentTable(models.Model):
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')

    class Meta:
        verbose_name = "Таблица для документа коммерческое предложение"
        verbose_name_plural = "Таблица для документа коммерческое предложение"

    def __str__(self):
        return self.name


class CommercialOfferDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Название')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_commercial')
    naming = models.CharField(max_length=150, verbose_name='Наименование',
                              help_text='Пример: на установку системы кондиционирования на 2 этаже', null=True,
                              blank=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', null=True, blank=True)
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(CommercialOfferDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Коммерческое предложение"
        verbose_name_plural = "Коммерческое предложение"

    def __str__(self):
        return f'{self.name} от {self.date}'


class OutlayDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    number_outlay = models.CharField(max_length=50, verbose_name='Номер сметы')
    name = models.CharField(max_length=150, verbose_name='Название')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_outlay')
    base = models.CharField(max_length=250, verbose_name='Основание',
                            help_text='Пример: к Договору № 114 от 04.12.2012 г.', null=True, blank=True)
    work_time = models.CharField(max_length=250, verbose_name='Срок выполнения работ',
                                 help_text='Пример: 1 месяц с даты подписания настоящего приложения', null=True,
                                 blank=True)
    name_construction = models.CharField(max_length=250, verbose_name='Наименование стройки',
                                         help_text='Пример: на установку системы кондиционирования на 2 этаже',
                                         null=True, blank=True)
    address = models.CharField(max_length=150, verbose_name='Адрес', null=True, blank=True)
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(CommercialOfferDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Смета"
        verbose_name_plural = "Смета"

    def __str__(self):
        return f'{self.name} от {self.date}'


class Ks2DocumentTable(models.Model):
    number_outlay = models.CharField(max_length=50, verbose_name='№ по смете', help_text='Введите № по смете',
                                     null=True, blank=True)
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    number_unit = models.CharField(max_length=50, verbose_name='№ ед. расц.', help_text='Введите № ед. расц.',
                                   null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')

    class Meta:
        verbose_name = "Таблица для документа КС-2"
        verbose_name_plural = "Таблица для документа КС-2"

    def __str__(self):
        return self.name


class Ks2Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Акт о приемке работ КС-2 №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_ks2')
    investor = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Инвестор',
                                 related_name='as_investor', null=True, blank=True)
    name_construction = models.CharField(max_length=250, verbose_name='Наименование стройки', null=True, blank=True)
    address_construction = models.CharField(max_length=150, verbose_name='Адрес стройки', null=True, blank=True)
    name_object = models.CharField(max_length=150, verbose_name='Наименование объекта', null=True, blank=True)
    view_okdp = models.CharField(max_length=150, verbose_name='Вид деятельности по ОКДП', null=True, blank=True)
    number_agreement = models.CharField(max_length=150, verbose_name='Номер договора подряда', null=True, blank=True)
    date_agreement = models.DateField(verbose_name='Дата договора подряда', null=True, blank=True)
    price_outlay = models.CharField(max_length=50, verbose_name='Сметная стоимость по договору', null=True, blank=True)
    period_from = models.DateField(verbose_name='Отчетный период с', null=True, blank=True)
    period_by = models.DateField(verbose_name='Отчетный период по', null=True, blank=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(Ks2DocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "КС-2"
        verbose_name_plural = "КС-2"

    def __str__(self):
        return f'{self.name} от {self.date}'


class Ks3DocumentTable(models.Model):
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование работ, затрат')
    code = models.CharField(max_length=50, verbose_name='Код', help_text='Введите код', null=True, blank=True)
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    price_from_construction = models.DecimalField(max_digits=12, decimal_places=2,
                                                  verbose_name='Стоимость с начала проведения работ',
                                                  help_text='Введите стоимость', null=True, blank=True)
    price_from_year = models.DecimalField(max_digits=12, decimal_places=2,
                                          verbose_name='Стоимость с начала года',
                                          help_text='Введите стоимость', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')

    class Meta:
        verbose_name = "Таблица для документа КС-3"
        verbose_name_plural = "Таблица для документа КС-3"

    def __str__(self):
        return self.name


class Ks3Document(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Справка КС-3 №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_ks3')
    investor = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Инвестор',
                                 related_name='as_investor_ks3', null=True, blank=True)
    name_construction = models.CharField(max_length=250, verbose_name='Наименование стройки', null=True, blank=True)
    address_construction = models.CharField(max_length=150, verbose_name='Адрес стройки', null=True, blank=True)
    number_agreement = models.CharField(max_length=150, verbose_name='Номер договора подряда', null=True, blank=True)
    date_agreement = models.DateField(verbose_name='Дата договора подряда', null=True, blank=True)
    period_from = models.DateField(verbose_name='Отчетный период с', null=True, blank=True)
    period_by = models.DateField(verbose_name='Отчетный период по', null=True, blank=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(Ks3DocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "КС-3"
        verbose_name_plural = "КС-3"

    def __str__(self):
        return f'{self.name} от {self.date}'


class ActServiceDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Акт оказания услуг №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_act_service')
    payment_for = models.CharField(max_length=150, verbose_name='Оплата за', null=True, blank=True)
    agreement = models.CharField(max_length=150, verbose_name='Договор', null=True, blank=True)
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(CommercialOfferDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Акт оказания услуг"
        verbose_name_plural = "Акт оказания услуг"

    def __str__(self):
        return f'{self.name} от {self.date}'


class PowerAttorneyDocumentTable(models.Model):
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')

    class Meta:
        verbose_name = "Таблица для документа доверенность"
        verbose_name_plural = "Таблица для документа доверенность"

    def __str__(self):
        return self.name


class PowerAttorneyDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Доверенность №')
    date = models.DateField(verbose_name='Дата выдачи')
    validity_period = models.DateField(verbose_name='Срок действия, до', null=True, blank=True)
    to_receive_from = models.CharField(max_length=150, verbose_name='На получение от', null=True, blank=True)
    according_document = models.CharField(max_length=150, verbose_name='По документу', null=True, blank=True)
    person_power = models.CharField(max_length=250, verbose_name='Лицо, получившее доверенность',
                                    help_text='Должность, Ф.И.О. полн. в дат. падеже', null=True, blank=True)
    passport_series = models.CharField(max_length=10, verbose_name='Серия паспорта', null=True, blank=True)
    passport_number = models.CharField(max_length=10, verbose_name='Номер паспорта', null=True, blank=True)
    issued_by = models.CharField(max_length=150, verbose_name='Кем выдан', null=True, blank=True)
    date_issue = models.DateField(verbose_name='Дата выдачи', null=True, blank=True)
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    bank_organization = models.ForeignKey(BankDetailsOrganization, on_delete=models.CASCADE,
                                          verbose_name='Банк организации', null=True, blank=True)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(PowerAttorneyDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Доверенность"
        verbose_name_plural = "Доверенность"

    def __str__(self):
        return f'{self.name} от {self.date}'


class SalesReceiptDocumentTable(models.Model):
    article_number = models.CharField(max_length=100, verbose_name='Артикул', help_text='Введите артикул', null=True,
                                      blank=True)
    name = models.TextField(verbose_name='Наименование', help_text='Введите наименование продукта')
    unit_of_measurement = models.CharField(max_length=10, verbose_name='Единица измерения',
                                           help_text='Введите единицу измерения')
    quantity = models.IntegerField(verbose_name='Количество', help_text='Введите количество товара')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена',
                                help_text='Введите стоимость товара')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Сумма')

    class Meta:
        verbose_name = "Таблица для документа товарный чек"
        verbose_name_plural = "Таблица для документа товарный чек"

    def __str__(self):
        return self.name


class SalesReceiptDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Чек №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    currency = models.CharField(max_length=100, verbose_name='Валюта', blank=True, null=True)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    table_product = models.ManyToManyField(SalesReceiptDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Товарный чек"
        verbose_name_plural = "Товарный чек"

    def __str__(self):
        return f'{self.name} от {self.date}'


class PkoDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Приходный кассовый ордер №')
    date = models.DateField(verbose_name='Дата создания')
    payer = models.CharField(max_length=250, verbose_name='Информация о плательщике', null=True, blank=True)
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    account_debit = models.CharField(max_length=150, verbose_name='Счет по дебету', null=True, blank=True)
    account_loan = models.CharField(max_length=150, verbose_name='Счет по кредиту', null=True, blank=True)
    summa = models.CharField(max_length=150, verbose_name='Сумма', null=True, blank=True)
    base = models.CharField(max_length=250, verbose_name='Основание',
                            help_text='Например: Расходная накладная № 123 от 17.12.2016', null=True, blank=True)
    annex = models.CharField(max_length=250, verbose_name='Приложение', null=True, blank=True)
    nds = models.IntegerField(verbose_name='Ставка НДС', null=True, blank=True, default=0)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)

    class Meta:
        verbose_name = "ПКО"
        verbose_name_plural = "ПКО"


class RkoDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Приходный кассовый ордер №')
    date = models.DateField(verbose_name='Дата создания')
    payer = models.CharField(max_length=250, verbose_name='Информация о получателе', null=True, blank=True)
    passport = models.CharField(max_length=250, verbose_name='Документ, удостоверяющий личность получателя', null=True,
                                blank=True)
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    account_debit = models.CharField(max_length=150, verbose_name='Счет по дебету', null=True, blank=True)
    account_loan = models.CharField(max_length=150, verbose_name='Счет по кредиту', null=True, blank=True)
    summa = models.CharField(max_length=150, verbose_name='Сумма', null=True, blank=True)
    base = models.CharField(max_length=250, verbose_name='Основание',
                            help_text='Например: Расходная накладная № 123 от 17.12.2016', null=True, blank=True)
    annex = models.CharField(max_length=250, verbose_name='Приложение', null=True, blank=True)
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)

    class Meta:
        verbose_name = "РКО"
        verbose_name_plural = "РКО"


class ReconciliationDocumentTable(models.Model):
    name_operation_org = models.TextField(verbose_name='Наименование операции, документы по данным организации')
    debit_org = models.CharField(max_length=50, verbose_name='Дебет (организация)')
    loan_org = models.CharField(max_length=50, verbose_name='Кредит (организация)')

    name_operation_counterparty = models.TextField(verbose_name='Наименование операции, документы по данным контрагента', null=True, blank=True)
    debit_counterparty = models.CharField(max_length=50, verbose_name='Дебет (контрагент)', null=True, blank=True)
    loan_counterparty = models.CharField(max_length=50, verbose_name='Кредит (контрагент)', null=True, blank=True)

    class Meta:
        verbose_name = "Таблица для документа акт сверки взаиморасчетов"
        verbose_name_plural = "Таблица для документа акт сверки взаиморасчетов"

    def __str__(self):
        return self.name_operation_org


class ReconciliationDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Акт сверки №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Контрагент',
                                     related_name='as_counterparty_reconciliation')
    period_from = models.DateField(verbose_name='Период с', null=True, blank=True)
    period_by = models.DateField(verbose_name='Период по', null=True, blank=True)
    balance_debit = models.CharField(max_length=150, verbose_name='Дебетовое сальдо', null=True, blank=True)
    balance_loan = models.CharField(max_length=150, verbose_name='Кредитовое сальдо', null=True, blank=True)
    place_of_act = models.CharField(max_length=150, verbose_name='Место подписания акта', null=True, blank=True)
    table_product = models.ManyToManyField(ReconciliationDocumentTable, verbose_name='Таблица товаров')

    class Meta:
        verbose_name = "Акт сверки взаиморасчетов"
        verbose_name_plural = "Акт сверки взаиморасчетов"

    def __str__(self):
        return f'{self.name} от {self.date}'


class AgreementDocument(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             help_text='Выберите пользователя')
    name = models.CharField(max_length=150, verbose_name='Договор №')
    date = models.DateField(verbose_name='Дата создания')
    organization = models.ForeignKey(InformationOrganization, on_delete=models.CASCADE, verbose_name='Организация')
    bank_organization = models.ForeignKey(BankDetailsOrganization, on_delete=models.CASCADE,
                                          verbose_name='Банк организации', help_text='Выберите банк организации',
                                          null=True, blank=True)
    counterparty = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='Покупатль',
                                     related_name='as_counterparty_agreement')
    bank_counterparty = models.ForeignKey(BankDetailsBuyer, on_delete=models.CASCADE, verbose_name='Банк покупателя',
                                          null=True, blank=True)
    sample = models.CharField(max_length=100, verbose_name='Шаблон')
    is_stamp = models.BooleanField(verbose_name='Добавить печать и подпись', null=True, blank=True, default=False)
    dop_field = models.ManyToManyField('ValueLabel', null=True, blank=True, verbose_name='Доп.поля')

    class Meta:
        verbose_name = "Договор/Документ"
        verbose_name_plural = "Договор/Документ"

    def __str__(self):
        return f'{self.name} от {self.date}'


class TemplateDocument(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название шаблона')
    content = models.TextField(verbose_name='Содержание документа')
    labels = models.ManyToManyField('LabelTemplateDocument', null=True, blank=True, verbose_name='Метки в документе')

    class Meta:
        verbose_name = "Шаблон для документа/договора"
        verbose_name_plural = "Шаблоны для документов/договоров"

    def __str__(self):
        return self.title


class LabelTemplateDocument(models.Model):
    label_code = models.CharField(max_length=500, verbose_name='Метка')
    label_desc = models.CharField(max_length=500, verbose_name='Комментарий к метке')

    class Meta:
        verbose_name = "Метка для шаблона"
        verbose_name_plural = "Метки для шаблонов"

    def __str__(self):
        return f'{self.label_code} | {self.label_desc}'


class ValueLabel(models.Model):
    label = models.ForeignKey(LabelTemplateDocument, on_delete=models.CASCADE, verbose_name='Метка')
    value = models.TextField(verbose_name='Значение метки')

    class Meta:
        verbose_name = "Значение метки"
        verbose_name_plural = "Значения меток"

    def __str__(self):
        return f'{self.label.label_code} | {self.value}'
