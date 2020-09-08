from django.db import models
from django.contrib.auth.models import User
import pytz

# Create your models here.

class Role(models.Model):
    id         = models.AutoField(primary_key=True)
    name       = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.SmallIntegerField(default=1)

    def __str__(self):
        return '%s' % self.name 

class Employee(models.Model):
	id       = models.AutoField(primary_key=True)
	name     = models.CharField(max_length=300)
	role     = models.ForeignKey(Role,on_delete=models.CASCADE)
	salary   = models.CharField(max_length=300, null=True, blank=True)
	address  = models.CharField(max_length=300)
	emp_id   = models.CharField(max_length=300, null=True, blank=True)
	phone_no = models.CharField(max_length=300)
	leaves   = models.IntegerField()
	auth_tbl = models.OneToOneField(User, on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s' % self.name


class Rate(models.Model):
	id                  = models.AutoField(primary_key=True)
	base_ir             = models.CharField(max_length=300, null=True, blank=True) 
	base_br             = models.CharField(max_length=200, null=True, blank=True)

	total_pay           = models.CharField(max_length=200, null=True, blank=True)

	difficultnp         = models.CharField(max_length=300, null=True, blank=True)
	extra_hours         = models.CharField(max_length=300, null=True, blank=True)
	file_attach         = models.CharField(max_length=300, null=True, blank=True)
	add_auth_days       = models.CharField(max_length=300, null=True, blank=True)

	new_entities_added  = models.CharField(max_length=300, null=True, blank=True)
	extra_days          = models.CharField(max_length=300, null=True, blank=True)

	duplicate_entities  = models.CharField(max_length=300, null=True, blank=True)
	errors              = models.CharField(max_length=300, null=True, blank=True)
	fines               = models.CharField(max_length=300, null=True, blank=True)

	duplicate_solic     = models.CharField(max_length=300)
	entity_cont_wrong   = models.CharField(max_length=300)
	false_referal       = models.CharField(max_length=300)
	fraudsolic_update   = models.CharField(max_length=300)
	source_ret_wo_res   = models.CharField(max_length=300)
	missed_bond         = models.CharField(max_length=300)
	missed_categories   = models.CharField(max_length=300)
	missed_solic_src    = models.CharField(max_length=300)
	missed_file         = models.CharField(max_length=300)
	missed_link         = models.CharField(max_length=300)
	missed_term         = models.CharField(max_length=300)
	not_posted_lead     = models.CharField(max_length=300)
	other_error         = models.CharField(max_length=300)
	other_serious_err   = models.CharField(max_length=300)
	refreshing_wds      = models.CharField(max_length=300)
	wage_not_selected   = models.CharField(max_length=300)
	skipped_solic       = models.CharField(max_length=300)
	source_ret_wo_note  = models.CharField(max_length=300)
	unjustified_absence = models.CharField(max_length=300)
	wrong_pre_bid       = models.CharField(max_length=300)
	wrong_categories    = models.CharField(max_length=300)
	wrong_geo_location  = models.CharField(max_length=300)
	incorrect_scope     = models.CharField(max_length=300)
	wrong_text_format   = models.CharField(max_length=300)
	auth_day_off        = models.CharField(max_length=300)
	unauth_day_off      = models.CharField(max_length=300)
	added_by            = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	added_date          = models.DateTimeField(auto_now_add=True)
	is_approved         = models.SmallIntegerField(default=0) 



class Invoice(models.Model):
	id                                 = models.AutoField(primary_key=True)
	invoice_date                       = models.DateField()
	monthdate                          = models.DateField()
	emp_type                           = models.CharField(max_length=150, null=True, blank=True)

	#ir invoice
	additional_auth_days               = models.CharField(max_length=100, default=0, blank=True)
	wds_source_checked_completely      = models.CharField(max_length=200, default=0, blank=True)
	new_solicitation_entered_correctly = models.CharField(max_length=200, default=0, blank=True)
	updated_solicitation_by_addenda    = models.CharField(max_length=200, default=0, blank=True)
	difficult_and_nonproductive_source = models.CharField(max_length=200, default=0, blank=True)
	extra_hours_worked                 = models.CharField(max_length=200, default=0, blank=True)
	file_attached                      = models.CharField(max_length=200, default=0, blank=True)

	#br invoice
	new_entities_added                 = models.CharField(max_length=200, default=0, blank=True)
	ph_added_to_bid_list               = models.CharField(max_length=200, default=0, blank=True)
	ph_edited_in_bid_list              = models.CharField(max_length=200, default=0, blank=True)
	ph_deleted_in_bid_list             = models.CharField(max_length=200, default=0, blank=True)
	extra_days_worked                  = models.CharField(max_length=200, default=0, blank=True)

	#fixed invoice
	total_pay                          = models.CharField(max_length=200, default=0, blank=True)

	authorised_day_off                 = models.CharField(max_length=200, default=0, blank=True)
	unauthorised_day_off               = models.CharField(max_length=200, default=0, blank=True)
	total_working_days                 = models.CharField(max_length=200, default=0, blank=True)
	total_days_worked                  = models.CharField(max_length=200, default=0, blank=True)

	#br_invoice
	duplicate_entities                 = models.CharField(max_length=200, default=0, blank=True)
	errors                             = models.CharField(max_length=200, default=0, blank=True)
	fines                              = models.CharField(max_length=200, default=0, blank=True)

	#ir and fixed invoice
	duplicate_solic                    = models.CharField(max_length=200, default=0, blank=True)
	entity_cont_wrong                  = models.CharField(max_length=200, default=0, blank=True)
	false_referal                      = models.CharField(max_length=200, default=0, blank=True)
	fraudulent_solicitation_update     = models.CharField(max_length=200, default=0, blank=True)
	source_returned_without_good_res   = models.CharField(max_length=200, default=0, blank=True)
	missed_bidbond_and_specs           = models.CharField(max_length=200, default=0, blank=True)
	missed_categories                  = models.CharField(max_length=200, default=0, blank=True)
	missed_solic_or_addend_from_source = models.CharField(max_length=200, default=0, blank=True)
	missed_incorrect_filetype          = models.CharField(max_length=200, default=0, blank=True)
	missing_or_wrong_outside_link      = models.CharField(max_length=200, default=0, blank=True)
	missing_or_wrong_term_contract     = models.CharField(max_length=200, default=0, blank=True)
	not_posted_as_lead                 = models.CharField(max_length=200, default=0, blank=True)
	other_error                        = models.CharField(max_length=200, default=0, blank=True)
	other_serious_error                = models.CharField(max_length=200, default=0, blank=True)
	refreshing_wds_page_to_diff_source = models.CharField(max_length=200, default=0, blank=True)
	prevailing_wage_not_selected       = models.CharField(max_length=200, default=0, blank=True)
	skipped_solicitation               = models.CharField(max_length=200, default=0, blank=True)
	source_returned_without_a_note     = models.CharField(max_length=200, default=0, blank=True)
	unexcused_unjustified_absence      = models.CharField(max_length=200, default=0, blank=True)
	wrongbid_prebid_mandatory          = models.CharField(max_length=200, default=0, blank=True)
	wrong_categories                   = models.CharField(max_length=200, default=0, blank=True)
	wrong_geographic_location          = models.CharField(max_length=200, default=0, blank=True)
	incomplete_and_incorrect_scope     = models.CharField(max_length=200, default=0, blank=True)
	wrong_text_format                  = models.CharField(max_length=200, default=0, blank=True)
	total_deduction                    = models.CharField(max_length=200, default=0, blank=True)
	total_payable                      = models.CharField(max_length=200, default=0, blank=True)
	emp_ownwer                         = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	rate                               = models.ForeignKey(Rate, on_delete=models.SET_NULL, null=True, blank=True)
	is_approved                        = models.SmallIntegerField(default=0)


