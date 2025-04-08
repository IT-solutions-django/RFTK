# Generated by Django 5.1.5 on 2025-04-07 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0068_templatedocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabelTemplateDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_code', models.CharField(max_length=500, verbose_name='Метка')),
                ('label_desc', models.CharField(max_length=500, verbose_name='Комментарий к метке')),
            ],
            options={
                'verbose_name': 'Метка для шаблона',
                'verbose_name_plural': 'Метки для шаблонов',
            },
        ),
        migrations.AlterModelOptions(
            name='templatedocument',
            options={'verbose_name': 'Шаблон для документа/договора', 'verbose_name_plural': 'Шаблоны для документов/договоров'},
        ),
    ]
