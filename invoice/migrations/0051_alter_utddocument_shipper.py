# Generated by Django 5.1.5 on 2025-02-21 05:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0050_alter_utddocumenttable_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utddocument',
            name='shipper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_shipper_utd', to='invoice.informationorganization', verbose_name='Грузоотправитель'),
        ),
    ]
