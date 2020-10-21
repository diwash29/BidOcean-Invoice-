# Generated by Django 2.2.5 on 2020-10-12 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_invoice', '0005_auto_20201003_0506'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('source', models.CharField(max_length=200)),
                ('entries', models.CharField(blank=True, max_length=300, null=True)),
                ('addendum', models.CharField(blank=True, max_length=300, null=True)),
                ('import_report', models.CharField(blank=True, max_length=300, null=True)),
                ('import_reject', models.CharField(blank=True, max_length=300, null=True)),
                ('solic_no', models.TextField(blank=True, null=True)),
                ('file_attach', models.CharField(blank=True, max_length=200, null=True)),
                ('wds_per_day', models.CharField(max_length=200)),
                ('usd', models.CharField(max_length=200)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_invoice.Employee')),
            ],
        ),
    ]