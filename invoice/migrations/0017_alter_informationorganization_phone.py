# Generated by Django 5.1.5 on 2025-02-04 16:54

import invoice.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0016_alter_informationorganization_kpp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informationorganization',
            name='phone',
            field=models.CharField(help_text='Введите телефон организации', max_length=50, validators=[invoice.models.validate_phone], verbose_name='Телефон'),
        ),
    ]
