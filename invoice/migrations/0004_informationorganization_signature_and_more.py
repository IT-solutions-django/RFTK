# Generated by Django 5.1.5 on 2025-01-30 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_informationorganization_stamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='informationorganization',
            name='signature',
            field=models.ImageField(blank=True, help_text='Добавьте подпись', null=True, upload_to='signatures', verbose_name='Подпись'),
        ),
        migrations.AlterField(
            model_name='informationorganization',
            name='stamp',
            field=models.ImageField(blank=True, help_text='Добавьте печать', upload_to='stamps', verbose_name='Печать'),
        ),
    ]
