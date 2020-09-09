# Generated by Django 2.2.5 on 2020-09-09 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('salary', models.CharField(blank=True, max_length=300, null=True)),
                ('address', models.CharField(max_length=300)),
                ('emp_id', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_no', models.CharField(max_length=300)),
                ('leaves', models.IntegerField()),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('auth_tbl', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('base_ir', models.CharField(blank=True, max_length=300, null=True)),
                ('base_br', models.CharField(blank=True, max_length=200, null=True)),
                ('total_pay', models.CharField(blank=True, max_length=200, null=True)),
                ('difficultnp', models.CharField(blank=True, max_length=300, null=True)),
                ('extra_hours', models.CharField(blank=True, max_length=300, null=True)),
                ('file_attach', models.CharField(blank=True, max_length=300, null=True)),
                ('add_auth_days', models.CharField(blank=True, max_length=300, null=True)),
                ('new_entities_added', models.CharField(blank=True, max_length=300, null=True)),
                ('extra_days', models.CharField(blank=True, max_length=300, null=True)),
                ('duplicate_entities', models.CharField(blank=True, max_length=300, null=True)),
                ('errors', models.CharField(blank=True, max_length=300, null=True)),
                ('fines', models.CharField(blank=True, max_length=300, null=True)),
                ('duplicate_solic', models.CharField(max_length=300)),
                ('entity_cont_wrong', models.CharField(max_length=300)),
                ('false_referal', models.CharField(max_length=300)),
                ('fraudsolic_update', models.CharField(max_length=300)),
                ('source_ret_wo_res', models.CharField(max_length=300)),
                ('missed_bond', models.CharField(max_length=300)),
                ('missed_categories', models.CharField(max_length=300)),
                ('missed_solic_src', models.CharField(max_length=300)),
                ('missed_file', models.CharField(max_length=300)),
                ('missed_link', models.CharField(max_length=300)),
                ('missed_term', models.CharField(max_length=300)),
                ('not_posted_lead', models.CharField(max_length=300)),
                ('other_error', models.CharField(max_length=300)),
                ('other_serious_err', models.CharField(max_length=300)),
                ('refreshing_wds', models.CharField(max_length=300)),
                ('wage_not_selected', models.CharField(max_length=300)),
                ('skipped_solic', models.CharField(max_length=300)),
                ('source_ret_wo_note', models.CharField(max_length=300)),
                ('unjustified_absence', models.CharField(max_length=300)),
                ('wrong_pre_bid', models.CharField(max_length=300)),
                ('wrong_categories', models.CharField(max_length=300)),
                ('wrong_geo_location', models.CharField(max_length=300)),
                ('incorrect_scope', models.CharField(max_length=300)),
                ('wrong_text_format', models.CharField(max_length=300)),
                ('auth_day_off', models.CharField(max_length=300)),
                ('unauth_day_off', models.CharField(max_length=300)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.SmallIntegerField(default=0)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_invoice.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_date', models.DateField()),
                ('monthdate', models.DateField()),
                ('emp_type', models.CharField(blank=True, max_length=150, null=True)),
                ('additional_auth_days', models.CharField(blank=True, default=0, max_length=100)),
                ('wds_source_checked_completely', models.CharField(blank=True, default=0, max_length=200)),
                ('new_solicitation_entered_correctly', models.CharField(blank=True, default=0, max_length=200)),
                ('updated_solicitation_by_addenda', models.CharField(blank=True, default=0, max_length=200)),
                ('difficult_and_nonproductive_source', models.CharField(blank=True, default=0, max_length=200)),
                ('extra_hours_worked', models.CharField(blank=True, default=0, max_length=200)),
                ('file_attached', models.CharField(blank=True, default=0, max_length=200)),
                ('new_entities_added', models.CharField(blank=True, default=0, max_length=200)),
                ('ph_added_to_bid_list', models.CharField(blank=True, default=0, max_length=200)),
                ('ph_edited_in_bid_list', models.CharField(blank=True, default=0, max_length=200)),
                ('ph_deleted_in_bid_list', models.CharField(blank=True, default=0, max_length=200)),
                ('extra_days_worked', models.CharField(blank=True, default=0, max_length=200)),
                ('total_pay', models.CharField(blank=True, default=0, max_length=200)),
                ('authorised_day_off', models.CharField(blank=True, default=0, max_length=200)),
                ('unauthorised_day_off', models.CharField(blank=True, default=0, max_length=200)),
                ('total_working_days', models.CharField(blank=True, default=0, max_length=200)),
                ('total_days_worked', models.CharField(blank=True, default=0, max_length=200)),
                ('duplicate_entities', models.CharField(blank=True, default=0, max_length=200)),
                ('errors', models.CharField(blank=True, default=0, max_length=200)),
                ('fines', models.CharField(blank=True, default=0, max_length=200)),
                ('duplicate_solic', models.CharField(blank=True, default=0, max_length=200)),
                ('entity_cont_wrong', models.CharField(blank=True, default=0, max_length=200)),
                ('false_referal', models.CharField(blank=True, default=0, max_length=200)),
                ('fraudulent_solicitation_update', models.CharField(blank=True, default=0, max_length=200)),
                ('source_returned_without_good_res', models.CharField(blank=True, default=0, max_length=200)),
                ('missed_bidbond_and_specs', models.CharField(blank=True, default=0, max_length=200)),
                ('missed_categories', models.CharField(blank=True, default=0, max_length=200)),
                ('missed_solic_or_addend_from_source', models.CharField(blank=True, default=0, max_length=200)),
                ('missed_incorrect_filetype', models.CharField(blank=True, default=0, max_length=200)),
                ('missing_or_wrong_outside_link', models.CharField(blank=True, default=0, max_length=200)),
                ('missing_or_wrong_term_contract', models.CharField(blank=True, default=0, max_length=200)),
                ('not_posted_as_lead', models.CharField(blank=True, default=0, max_length=200)),
                ('other_error', models.CharField(blank=True, default=0, max_length=200)),
                ('other_serious_error', models.CharField(blank=True, default=0, max_length=200)),
                ('refreshing_wds_page_to_diff_source', models.CharField(blank=True, default=0, max_length=200)),
                ('prevailing_wage_not_selected', models.CharField(blank=True, default=0, max_length=200)),
                ('skipped_solicitation', models.CharField(blank=True, default=0, max_length=200)),
                ('source_returned_without_a_note', models.CharField(blank=True, default=0, max_length=200)),
                ('unexcused_unjustified_absence', models.CharField(blank=True, default=0, max_length=200)),
                ('wrongbid_prebid_mandatory', models.CharField(blank=True, default=0, max_length=200)),
                ('wrong_categories', models.CharField(blank=True, default=0, max_length=200)),
                ('wrong_geographic_location', models.CharField(blank=True, default=0, max_length=200)),
                ('incomplete_and_incorrect_scope', models.CharField(blank=True, default=0, max_length=200)),
                ('wrong_text_format', models.CharField(blank=True, default=0, max_length=200)),
                ('total_deduction', models.CharField(blank=True, default=0, max_length=200)),
                ('total_payable', models.CharField(blank=True, default=0, max_length=200)),
                ('is_approved', models.SmallIntegerField(default=0)),
                ('emp_ownwer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_invoice.Employee')),
                ('rate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_invoice.Rate')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_invoice.Role'),
        ),
    ]
