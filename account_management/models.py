from django.db import models
from django.contrib.auth.models import User
#from manage_user.models import Userdetail
from user_invoice.models import Employee
import pytz

# Create your models here.

class AccountDetails(models.Model):
    id         = models.AutoField(primary_key=True)
    acc_no     = models.CharField(max_length=200)
    bank       = models.CharField(max_length=200)
    other_bank = models.CharField(max_length=300, null=True, blank=True)
    ifsc_other = models.CharField(max_length=300, null=True, blank=True)
    employee   = models.ForeignKey(Employee,on_delete=models.CASCADE, related_name='employee_accounts')
    created_at = models.DateTimeField(auto_now_add=True)
    status     = models.SmallIntegerField(default=1)

    def __str__(self):
        return '%s' % self.acc_no 