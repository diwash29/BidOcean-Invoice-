# Generated by Django 2.2.5 on 2020-10-14 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_invoice', '0007_auto_20201014_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='wds_edit',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='wds_import',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='wds_solicitaion',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='wds_source',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
