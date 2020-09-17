from django.db import models
from django.contrib.auth.models import User
import pytz
from user_invoice.models import Employee

# Create your models here.

class LeaveBalance(models.Model):
	id           = models.AutoField(primary_key=True)
	casual_leave = models.CharField(max_length=200)
	earned_leave = models.CharField(max_length=200)
	sick_leave   = models.CharField(max_length=200)
	employee     = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='leave_bal')

class LeaveRequest(models.Model):
	id              = models.AutoField(primary_key=True)
	leave_type      = models.CharField(max_length=200)
	reason_msg      = models.TextField()
	employee        = models.ForeignKey(Employee, on_delete=models.CASCADE)
	available_days  = models.CharField(max_length=200)
	requesting_days = models.CharField(max_length=200)
	from_date       = models.DateField()
	to_date         = models.DateField()	
	status          = models.SmallIntegerField(default=0)