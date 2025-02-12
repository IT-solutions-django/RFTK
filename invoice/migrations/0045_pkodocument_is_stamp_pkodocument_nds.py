# Generated by Django 5.1.5 on 2025-02-11 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0044_salesreceiptdocument_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pkodocument',
            name='is_stamp',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Добавить печать и подпись'),
        ),
        migrations.AddField(
            model_name='pkodocument',
            name='nds',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Ставка НДС'),
        ),
    ]
