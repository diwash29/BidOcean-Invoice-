# Generated by Django 2.2.5 on 2020-10-03 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_auto_20200917_0628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leavebalance',
            old_name='casual_leave',
            new_name='others_leave',
        ),
        migrations.RenameField(
            model_name='leavebalance',
            old_name='earned_leave',
            new_name='paid_leave',
        ),
    ]