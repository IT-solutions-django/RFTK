# Generated by Django 5.1.5 on 2025-02-11 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0045_pkodocument_is_stamp_pkodocument_nds'),
    ]

    operations = [
        migrations.AddField(
            model_name='rkodocument',
            name='is_stamp',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Добавить печать и подпись'),
        ),
    ]
