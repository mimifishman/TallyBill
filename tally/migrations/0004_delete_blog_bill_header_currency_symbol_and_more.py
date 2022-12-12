# Generated by Django 4.0.4 on 2022-07-26 10:33

import django.contrib.auth.password_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0003_bill_header_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.AddField(
            model_name='bill_header',
            name='currency_symbol',
            field=models.CharField(default='$', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.validate_password]),
        ),
    ]