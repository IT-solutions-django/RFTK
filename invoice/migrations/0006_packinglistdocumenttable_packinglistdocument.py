# Generated by Django 5.1.5 on 2025-02-01 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_vatinvoicedocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackingListDocumentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(help_text='Введите наименование продукта', verbose_name='Наименование')),
                ('product_code', models.CharField(help_text='Введите код товара', max_length=50, verbose_name='Код товара')),
                ('unit_of_measurement', models.CharField(help_text='Введите единицу измерения', max_length=10, verbose_name='Единица измерения')),
                ('type_of_packaging', models.CharField(help_text='Введите вид упаковки', max_length=100, verbose_name='Вид упаковки')),
                ('quantity', models.IntegerField(help_text='Введите количество товара', verbose_name='Количество')),
                ('gross_weight', models.IntegerField(help_text='Введите масса брутто', verbose_name='Масса брутто')),
                ('net_weight', models.IntegerField(help_text='Введите масса нетто', verbose_name='Масса нетто')),
                ('price', models.DecimalField(decimal_places=2, help_text='Введите стоимость товара', max_digits=6, verbose_name='Цена')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Сумма')),
            ],
        ),
        migrations.CreateModel(
            name='PackingListDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('date', models.DateField(verbose_name='Дата создания')),
                ('structural_division', models.CharField(max_length=500, verbose_name='Структурное подразделение')),
                ('base', models.CharField(max_length=500, verbose_name='Основание')),
                ('number_base', models.CharField(max_length=100, verbose_name='Номер основания')),
                ('date_base', models.DateField(verbose_name='Дата основания')),
                ('packing_list', models.CharField(max_length=250, verbose_name='Транспортная накладная')),
                ('date_packing_list', models.DateField(verbose_name='Дата')),
                ('shipping_date', models.DateField(verbose_name='Дата отгрузки')),
                ('date_of_receipt', models.DateField(verbose_name='Дата получения')),
                ('bank_counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.bankdetailsbuyer', verbose_name='Банк контрагента')),
                ('bank_organization', models.ForeignKey(help_text='Выберите банк организации', on_delete=django.db.models.deletion.CASCADE, to='invoice.bankdetailsorganization', verbose_name='Банк организации')),
                ('consignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_consignee_packing', to='invoice.buyer', verbose_name='Грузополучатель')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_counterparty_packing', to='invoice.buyer', verbose_name='Контрагент')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.informationorganization', verbose_name='Организация')),
                ('shipper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_shipper_packing', to='invoice.buyer', verbose_name='Грузоотправитель')),
                ('table_product', models.ManyToManyField(to='invoice.packinglistdocumenttable', verbose_name='Таблица товаров')),
            ],
        ),
    ]
