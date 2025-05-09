# Generated by Django 5.1.5 on 2025-02-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_commercialofferdocument_user_invoicedocument_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicedocumenttable',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='invoicedocumenttable',
            name='discount',
            field=models.DecimalField(decimal_places=2, help_text='Введите скидку на товар', max_digits=12, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='invoicedocumenttable',
            name='price',
            field=models.DecimalField(decimal_places=2, help_text='Введите стоимость товара', max_digits=12, verbose_name='Цена'),
        ),
    ]
