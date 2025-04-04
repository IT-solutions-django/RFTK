# Generated by Django 5.1.5 on 2025-02-28 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0064_alter_rkodocument_account_debit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='phone',
            field=models.CharField(blank=True, help_text='Введите телефон организации покупателя', max_length=50, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='informationorganization',
            name='phone',
            field=models.CharField(blank=True, help_text='Введите телефон организации', max_length=50, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='utddocumenttable',
            name='quantity',
            field=models.FloatField(help_text='Введите количество товара', verbose_name='Количество'),
        ),
    ]
