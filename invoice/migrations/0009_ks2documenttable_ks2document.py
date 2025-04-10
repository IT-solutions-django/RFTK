# Generated by Django 5.1.5 on 2025-02-03 10:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0008_alter_commercialofferdocument_naming_outlaydocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ks2DocumentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_outlay', models.CharField(help_text='Введите № по смете', max_length=50, verbose_name='№ по смете')),
                ('name', models.TextField(help_text='Введите наименование продукта', verbose_name='Наименование')),
                ('number_unit', models.CharField(help_text='Введите № ед. расц.', max_length=50, verbose_name='№ ед. расц.')),
                ('unit_of_measurement', models.CharField(help_text='Введите единицу измерения', max_length=10, verbose_name='Единица измерения')),
                ('quantity', models.IntegerField(help_text='Введите количество товара', verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, help_text='Введите стоимость товара', max_digits=6, verbose_name='Цена')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Сумма')),
            ],
        ),
        migrations.CreateModel(
            name='Ks2Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('date', models.DateField(verbose_name='Дата создания')),
                ('name_construction', models.CharField(max_length=250, verbose_name='Наименование стройки')),
                ('address_construction', models.CharField(max_length=150, verbose_name='Адрес стройки')),
                ('name_object', models.CharField(max_length=150, verbose_name='Наименование объекта')),
                ('view_okdp', models.CharField(max_length=150, verbose_name='Вид деятельности по ОКДП')),
                ('number_agreement', models.CharField(max_length=150, verbose_name='Номер договора подряда')),
                ('date_agreement', models.DateField(verbose_name='Дата договора подряда')),
                ('price_outlay', models.CharField(max_length=50, verbose_name='Сметная стоимость по договору')),
                ('period_from', models.DateField(verbose_name='Отчетный период с')),
                ('period_by', models.DateField(verbose_name='Отчетный период по')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_counterparty_ks2', to='invoice.buyer', verbose_name='Контрагент')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_investor', to='invoice.buyer', verbose_name='Инвестор')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.informationorganization', verbose_name='Организация')),
                ('table_product', models.ManyToManyField(to='invoice.ks2documenttable', verbose_name='Таблица товаров')),
            ],
        ),
    ]
