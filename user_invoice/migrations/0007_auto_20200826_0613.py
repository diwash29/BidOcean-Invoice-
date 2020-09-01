# Generated by Django 2.2.5 on 2020-08-26 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_invoice', '0006_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='authorized_day_off',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='emp_ownwer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_invoice.Employee'),
        ),
    ]