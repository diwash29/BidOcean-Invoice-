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
	phone_no = models.CharField(max_length=300)
	leaves   = models.IntegerField()
	auth_tbl = models.OneToOneField(User, on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '%s' % self.name


class Rate(models.Model):
	id                  = models.AutoField(primary_key=True)
	base                = models.CharField(max_length=300, null=True, blank=True)  
	difficultnp         = models.CharField(max_length=300, null=True, blank=True)
	extra_hours         = models.CharField(max_length=300, null=True, blank=True)
	file_attach         = models.CharField(max_length=300, null=True, blank=True)

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
	is_approved         = models.SmallIntegerField(default=0) 