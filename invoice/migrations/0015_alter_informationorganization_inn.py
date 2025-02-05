# Generated by Django 5.1.5 on 2025-02-04 13:54

import invoice.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0014_alter_commercialofferdocumenttable_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationorganization',
            name='inn',
            field=models.CharField(help_text='Введите ИНН организации', max_length=50, validators=[invoice.models.validate_inn], verbose_name='ИНН'),
        ),
    ]
