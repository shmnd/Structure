from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from datetime import timezone,timedelta
# Create your models here.

class AbstractDateFieldMix(models.Model):
    created_date              = models.DateTimeField( auto_now_add=True, editable=False, blank=True, null=True)
    modified_date             = models.DateTimeField( auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser,PermissionsMixin,AbstractDateFieldMix):

    class GenderType(models.TextChoices):
        male = "Male"
        female = "Female"
        other = "Other"

    email               = models.EmailField(unique=True, null=True,blank=True)
    user_name           = models.CharField(unique=True,null=True,blank=True,max_length=100)
    date_joined         = models.DateTimeField(null=True,blank=True)
    first_name          = models.CharField(max_length=100,blank=True,null=True)
    last_login          = models.DateTimeField(null=True,blank=True)
    is_active           = models.BooleanField(default=True)
    profile_image       = models.FileField(blank=True, null=True)
    gender              = models.CharField(choices=GenderType.choices,blank=True,null=True,default=GenderType.other)
    phone_number        = models.CharField(max_length=15,blank=True,null=True)
    password            = models.CharField(max_length=225,blank=True,null=True,editable=False)
    confirm_password    = models.CharField(max_length=225,blank=True,null=True,editable=False)
    otp                 = models.CharField(max_length=6,blank=True,null=True)    
    otp_expiry          = models.DateTimeField(blank=True,null=True)
    is_admin           = models.BooleanField(default=False,blank=True, null=True)
    is_doctor          = models.BooleanField(default=False,blank=True, null=True)
    department         = models.CharField(max_length=100,blank=True,null=True)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']


    def set_otp(self,otp):
        self.otp = otp
        self.otp_expiry = timezone.now() + timedelta(minutes=5) #expires in 5 mintues

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class GeneratedAccessToken(AbstractDateFieldMix):
    token = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.token

    


    