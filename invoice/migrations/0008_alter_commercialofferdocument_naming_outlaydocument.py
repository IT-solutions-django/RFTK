# Generated by Django 5.1.5 on 2025-02-03 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_commercialofferdocumenttable_commercialofferdocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialofferdocument',
            name='naming',
            field=models.CharField(help_text='Пример: на установку системы кондиционирования на 2 этаже', max_length=150, verbose_name='Наименование'),
        ),
        migrations.CreateModel(
            name='OutlayDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_outlay', models.CharField(max_length=50, verbose_name='Номер сметы')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('date', models.DateField(verbose_name='Дата создания')),
                ('base', models.CharField(help_text='Пример: к Договору № 114 от 04.12.2012 г.', max_length=250, verbose_name='Основание')),
                ('work_time', models.CharField(help_text='Пример: 1 месяц с даты подписания настоящего приложения', max_length=250, verbose_name='Срок выполнения работ')),
                ('name_construction', models.CharField(help_text='Пример: на установку системы кондиционирования на 2 этаже', max_length=250, verbose_name='Наименование стройки')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_counterparty_outlay', to='invoice.buyer', verbose_name='Контрагент')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.informationorganization', verbose_name='Организация')),
                ('table_product', models.ManyToManyField(to='invoice.commercialofferdocumenttable', verbose_name='Таблица товаров')),
            ],
        ),
    ]
