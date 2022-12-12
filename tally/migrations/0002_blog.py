# Generated by Django 4.0.4 on 2022-07-21 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tally', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='documents/')),
            ],
        ),
    ]
