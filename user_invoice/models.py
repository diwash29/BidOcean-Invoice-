from django.db import models
from django.contrib.auth.models import User
from manage_user.models import Userdetail
# from account_management.models import AccountDetails
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
	id          = models.AutoField(primary_key=True)
	name        = models.CharField(max_length=300)
	role        = models.ForeignKey(Role,on_delete=models.CASCADE)
	salary      = models.CharField(max_length=300, null=True, blank=True)
	address     = models.CharField(max_length=300)
	emp_id      = models.CharField(max_length=300, null=True, blank=True)
	phone_no    = models.CharField(max_length=300)
	designation = models.CharField(max_length=300, null=True, blank=True)
	# leaves   = models.IntegerField()
	auth_tbl    = models.OneToOneField(Userdetail, on_delete=models.CASCADE)
	added_at    = models.DateTimeField(auto_now_add=True)
	is_manager  = models.SmallIntegerField(default=0)
	report_to   = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='empreport_to')

	def __str__(self):
		return '%s' % self.name


class Rate(models.Model):
	id                  = models.AutoField(primary_key=True)
	
	file_attach         = models.CharField(max_length=300, null=True, blank=True)
	
	wds_solicitaion     = models.CharField(max_length=300, null=True, blank=True)
	wds_source          = models.CharField(max_length=300, null=True, blank=True)
	wds_edit            = models.CharField(max_length=300, null=True, blank=True)
	wds_import          = models.CharField(max_length=300, null=True, blank=True)

	
	auth_day_off        = models.CharField(max_length=300)
	unauth_day_off      = models.CharField(max_length=300)
	added_by            = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
	added_date          = models.DateTimeField(auto_now_add=True)
	is_approved         = models.SmallIntegerField(default=0) 



class Invoice(models.Model):
	id                         = models.AutoField(primary_key=True)
	invoice_date               = models.DateField()
	monthdate                  = models.DateField()

	production_pay_deduction   = models.CharField(max_length=200, default=0, blank=True)
	wds_solicitaion            = models.CharField(max_length=200, default=0, blank=True)
	wds_source                 = models.CharField(max_length=200, default=0, blank=True)
	wds_edit                   = models.CharField(max_length=200, default=0, blank=True)
	wds_import                 = models.CharField(max_length=200, default=0, blank=True)
	file_upload                = models.CharField(max_length=200, default=0, blank=True)
	fixed_salary               = models.CharField(max_length=200, default=0, blank=True)
	
	wds_solicitaion_rate       = models.CharField(max_length=200, default=0, blank=True)
	wds_source_rate            = models.CharField(max_length=200, default=0, blank=True)
	wds_edit_rate              = models.CharField(max_length=200, default=0, blank=True)
	wds_import_rate            = models.CharField(max_length=200, default=0, blank=True)
	auth_day_rate              = models.CharField(max_length=200, default=0, blank=True)

	bank_account               = models.ForeignKey('account_management.AccountDetails', on_delete=models.SET_NULL, null=True, blank=True)

	percent_deduction          = models.CharField(max_length=200, default=0, blank=True)

	authorised_day_off         = models.CharField(max_length=200, default=0, blank=True)
	unauthorised_day_off       = models.CharField(max_length=200, default=0, blank=True)

	emp_pf_id                  = models.CharField(max_length=200, default=0, blank=True)
	emp_esi_id                 = models.CharField(max_length=200, default=0, blank=True)
	dollar_rate                = models.CharField(max_length=200, default=0, blank=True)

	emp_ins_fund               = models.CharField(max_length=200, default=0, blank=True)
	percent_pf_prev_month      = models.CharField(max_length=200, default=0, blank=True)
	advance                    = models.CharField(max_length=200, default=0, blank=True)

	commission                 = models.CharField(max_length=200, default=0, blank=True)
	
	total_deduction            = models.CharField(max_length=200, default=0, blank=True)
	total_payable              = models.CharField(max_length=200, default=0, blank=True)
	emp_ownwer                 = models.ForeignKey(Employee, on_delete=models.CASCADE)
	is_approved                = models.SmallIntegerField(default=0)

	def __str__(self):
		return '%s' % self.emp_ownwer+str(self.monthdate)

class ProductionReport(models.Model):
	id            = models.AutoField(primary_key=True)
	date          = models.DateField()
	source        = models.CharField(max_length=200)
	entries       = models.CharField(max_length=300, null=True, blank=True)
	addendum      = models.CharField(max_length=300, null=True, blank=True)
	import_report = models.CharField(max_length=300, null=True, blank=True)
	import_reject = models.CharField(max_length=300, null=True, blank=True)	
	solic_no      = models.TextField(null=True, blank=True)
	file_attach   = models.CharField(max_length=200, null=True, blank=True)
	wds_per_day   = models.CharField(max_length=200)
	usd           = models.CharField(max_length=200)
	employee      = models.ForeignKey(Employee, on_delete=models.CASCADE)


class MonthlyDeduction(models.Model):
	id                = models.AutoField(primary_key=True)
	month             = models.IntegerField(unique=True)
	deduction_percent = models.CharField(max_length=200)	
	is_approved       = models.SmallIntegerField(default=0)


class DollarRate(models.Model):
	id                = models.AutoField(primary_key=True)
	dollar_rate       = models.CharField(max_length=200)

	def __str__(self):
		return '%s' % self.dollar_rate







