from django.db import models
import pytz
from user_invoice.models import Employee
# Create your models here.


class ExpenseType(models.Model):
	id           = models.AutoField(primary_key=True)
	expense_type = models.CharField(max_length=200)
	added_date   = models.DateTimeField(auto_now_add=True)
	added_by     = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return '%s' % self.expense_type 


class Expenses(models.Model):
	id           = models.AutoField(primary_key=True)
	expense_date = models.DateTimeField(auto_now_add=True)
	expense_type = models.ForeignKey(ExpenseType,on_delete=models.CASCADE)
	amount       = models.CharField(max_length=200)
	bill_no      = models.CharField(max_length=200)
	remarks      = models.TextField(null=True, blank=True)
	added_by     = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return '%s' % self.bill_no 