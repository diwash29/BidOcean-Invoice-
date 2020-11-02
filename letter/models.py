from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class EmployeeDetail(models.Model):
    first_name              = models.CharField(max_length=200)
    last_name               = models.CharField(max_length=200)
    designation             = models.CharField(max_length=100)
    ctc                     = models.PositiveIntegerField()
    joining_date            = models.DateField(blank=False)
    email                   = models.EmailField(null=True,blank=True)
    phone_regex             = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Phone number must consist of 10 digits.(Like 1234567890)")
    phone                   = models.CharField(validators=[phone_regex],max_length=10,blank=True,null=True)
    created_at              = models.DateField(auto_now_add=True)


    def __str__(self):
        return '%s' % self.first_name+' '+self.last_name
        # return self.first_name+" "+self.last_name

    class Meta:
        verbose_name_plural = "Employee Details"
        ordering = ['-id']
