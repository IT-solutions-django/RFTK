# Generated by Django 5.1.5 on 2025-02-10 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0037_vatinvoicedocument_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='commercialofferdocument',
            name='currency',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='commercialofferdocument',
            name='is_stamp',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Добавить печать и подпись'),
        ),
        migrations.AddField(
            model_name='commercialofferdocument',
            name='nds',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Ставка НДС'),
        ),
    ]
