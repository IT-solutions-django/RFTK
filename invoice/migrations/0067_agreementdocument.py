# Generated by Django 5.1.5 on 2025-03-27 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0066_reconciliationdocumenttable_reconciliationdocument'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Договор №')),
                ('date', models.DateField(verbose_name='Дата создания')),
                ('sample', models.CharField(max_length=100, verbose_name='Шаблон')),
                ('time_supply', models.TextField(blank=True, null=True, verbose_name='Поставка товара в течении')),
                ('strength_supply', models.TextField(blank=True, null=True, verbose_name='Поставка товара осуществляется силами')),
                ('replace_price_supply', models.TextField(blank=True, null=True, verbose_name='Согласие об изменении стоимости в течение')),
                ('transition_time', models.TextField(blank=True, null=True, verbose_name='Право собственности переходит в момент подписания')),
                ('fine', models.TextField(blank=True, null=True, verbose_name='Штраф за не поставку товара за каждый день просрочки')),
                ('is_stamp', models.BooleanField(blank=True, default=False, null=True, verbose_name='Добавить печать и подпись')),
                ('bank_counterparty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.bankdetailsbuyer', verbose_name='Банк покупателя')),
                ('bank_organization', models.ForeignKey(blank=True, help_text='Выберите банк организации', null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.bankdetailsorganization', verbose_name='Банк организации')),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='as_counterparty_agreement', to='invoice.buyer', verbose_name='Покупатль')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.informationorganization', verbose_name='Организация')),
                ('user', models.ForeignKey(help_text='Выберите пользователя', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Договор/Документ',
                'verbose_name_plural': 'Договор/Документ',
            },
        ),
    ]
