# Generated by Django 3.2.4 on 2021-06-18 00:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='comissao',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)]),
        ),
    ]