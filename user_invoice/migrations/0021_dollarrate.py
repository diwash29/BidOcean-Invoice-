# Generated by Django 2.2.13 on 2020-10-28 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_invoice', '0020_auto_20201023_0522'),
    ]

    operations = [
        migrations.CreateModel(
            name='DollarRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dollar_rate', models.CharField(max_length=200)),
            ],
        ),
    ]