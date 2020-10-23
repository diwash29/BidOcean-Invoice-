from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
#from user_invoice.models import Role
#from LivingLibrary.models import Genre, Book
# from courses.models import Lesson
# from audios.models import Audio
# from softwares.models import Softwaredetail
from django.utils.timezone import now

# class Usertype(models.Model):
#     name = models.CharField(max_length=20)
#     def __str__(self):
#         return self.name
    
class Userdetail(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(max_length = 30, unique=True,null=True)
    firstname       = models.CharField(max_length = 30,null=True)
    lastname        = models.CharField(max_length = 30,null=True,blank=True)
    password        = models.TextField()
    phone           = models.CharField(max_length=200,null=True)
    email           = models.CharField(max_length=200,null=True)
    address         = models.CharField(max_length=300,null=True)
    designation     = models.CharField(max_length=300,null=True)
    role            = models.ForeignKey('user_invoice.Role', on_delete=models.SET_NULL, null=True, blank=True)
    employee_id     = models.CharField(max_length=200, null=True)
    salary          = models.CharField(max_length=200, null=True)
    is_manager      = models.SmallIntegerField(default=0)
    # report_to       = models.ForeignKey('user_invoice.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []
    objects         = CustomUserManager()

    def __str__(self):
        return self.username


# class UserActivity(models.Model):
#     user = models.ForeignKey('Userdetail', on_delete=models.CASCADE)
#     category = models.CharField(max_length=10)
#     catid = models.IntegerField()
#     book = models.ForeignKey('LivingLibrary.Book', on_delete=models.CASCADE, blank=True, null=True)
#     audio = models.ForeignKey('audios.Audio', on_delete=models.CASCADE, blank=True, null=True)
#     courses = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE, blank=True, null=True)
#     softwares = models.ForeignKey('softwares.Softwaredetail', on_delete=models.CASCADE, blank=True, null=True)
#     viewed = models.DateTimeField(default=now, blank=True)
#     downloads = models.BooleanField(blank=True,null=True)
#     def __str__(self):
#         return str(self.user)+ " "+self.category+" "+str(self.catid)