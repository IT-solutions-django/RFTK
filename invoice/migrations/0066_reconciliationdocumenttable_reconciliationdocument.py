# Generated by Django 5.1.5 on 2025-03-27 04:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0065_alter_buyer_phone_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReconciliationDocumentTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_operation_org', models.TextField(verbose_name='Наименование операции, документы по данным организации')),
                ('debit_org', models.CharField(max_length=50, verbose_name='Дебет (организация)')),
                ('loan_org', models.CharField(max_length=50, verbose_name='Кредит (организация)')),
                ('name_operation_counterparty', models.TextField(blank=True, null=True, verbose_name='Наименование операции, документы по данным контрагента')),
                ('debit_counterparty', models.CharField(blank=True, max_length=50, null=True, verbose_name='Дебет (контрагент)')),
                ('loan_counterparty', models.CharField(blank=True, max_length=50, null=True, verbose_name='Кредит (контрагент)')),
            ],
            options={
                'verbose_name': 'Таблица для документа акт сверки взаиморасчетов',
                'verbose_name_plural': 'Таблица для документа акт сверки взаиморасчетов',
            },
        ),
        migrations.CreateModel(
            name='ReconciliationDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Акт сверки №')),
                ('date', models.DateField(verbose_name='Дата создания')),
                ('period_from', models.DateField(blank=True, null=True, verbose_name='Период с')),
                ('period_by', models.DateField(blank=True, null=True, verbose_name='Период по')),
                ('balance_debit', models.CharField(blank=True, max_length=150, null=True, verbose_name='Дебетовое сальдо')),
                ('balance_loan', models.CharField(blank=True, max_length=150, null=True, verbose_name='Кредитовое сальдо')),
                ('place_of_act', models.CharField(blank=True, max_length=150, null=True, verbose_name='Место подписания акта')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_counterparty_reconciliation', to='invoice.buyer', verbose_name='Контрагент')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.informationorganization', verbose_name='Организация')),
                ('user', models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('table_product', models.ManyToManyField(to='invoice.reconciliationdocumenttable', verbose_name='Таблица товаров')),
            ],
            options={
                'verbose_name': 'Акт сверки взаиморасчетов',
                'verbose_name_plural': 'Акт сверки взаиморасчетов',
            },
        ),
    ]
