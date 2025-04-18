# Generated by Django 5.1.5 on 2025-02-06 09:24

import invoice.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0027_informationorganization_ogrnip_and_more'),
    ]

    operations = [

        migrations.AlterField(
            model_name='bankdetailsbuyer',
            name='current_account',
            field=models.CharField(default=1, help_text='Введите № расчетного счёта банка', max_length=100, validators=[invoice.models.validate_current_account], verbose_name='Расчетный счёт'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bankdetailsorganization',
            name='current_account',
            field=models.CharField(default=1, help_text='Введите № расчетного счёта банка', max_length=100, validators=[invoice.models.validate_current_account], verbose_name='Расчетный счёт'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyer',
            name='address',
            field=models.TextField(blank=True, help_text='Введите адрес организации покупателя', null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='kpp',
            field=models.CharField(blank=True, help_text='Введите КПП организации покупателя', max_length=50, null=True, validators=[invoice.models.validate_kpp], verbose_name='КПП'),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='ogrn',
            field=models.CharField(blank=True, help_text='Введите ОГРН организации покупателя', max_length=50, null=True, validators=[invoice.models.validate_ogrn], verbose_name='ОГРН'),
        ),
        migrations.AlterField(
            model_name='informationorganization',
            name='address',
            field=models.TextField(blank=True, help_text='Введите адрес организации', null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='informationorganization',
            name='position_at_work',
            field=models.CharField(blank=True, help_text='Введите должность руководителя организации', max_length=50, null=True, verbose_name='Должность руководителя'),
        ),
        migrations.AlterField(
            model_name='informationorganization',
            name='supervisor',
            field=models.CharField(blank=True, help_text='Введите ФИО руководителя организации', max_length=100, null=True, verbose_name='Руководитель'),
        ),
    ]
