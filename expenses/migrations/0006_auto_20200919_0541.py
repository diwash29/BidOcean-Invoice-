# Generated by Django 2.2.5 on 2020-09-19 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0005_merge_20200918_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
