from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from datetime import timezone,timedelta
from django.utils.translation import gettext_lazy as _
# Create your models here.

class AbstractDateFieldMix(models.Model):
    created_date              = models.DateTimeField( auto_now_add=True, editable=False, blank=True, null=True)
    modified_date             = models.DateTimeField( auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self,username,password=None,replica_db=None, **extra_fields):
        if not username:
            raise ValueError(_('Username must be set'))
        
        user = self.model(username=username,replica_db=replica_db,**extra_fields)

        if password:
            user.set_password(password.strip())

        user.save(using=replica_db)

        return user
    
    def create_superuser(self,username,password=None,repica_db=None,**extra_fields):
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True'))

        
        return self.create_user(username,password,**extra_fields)
        

class User(AbstractBaseUser,PermissionsMixin,AbstractDateFieldMix):

    class GenderType(models.TextChoices):
        male = "Male"
        female = "Female"
        other = "Other"

    email               = models.EmailField(unique=True, null=True,blank=True)
    username            = models.CharField(unique=True,null=True,blank=True,max_length=100)
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
    is_admin           = models.BooleanField(default=False)
    is_staff           = models.BooleanField(default=False)
    is_superuser           = models.BooleanField(default=False)
    is_doctor          = models.BooleanField(default=False)
    department         = models.CharField(max_length=100,blank=True,null=True)
    replica_db          = models.CharField(max_length=20,choices=[('replica_1','Replica_1'),('replica_2','Replica_2')],blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()


    def set_otp(self,otp):
        self.otp = otp
        self.otp_expiry = timezone.now() + timedelta(minutes=5) #expires in 5 mintues

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # def __str__(self):
    #     return self.username if self.username else "Unnamed User"


class GeneratedAccessToken(AbstractDateFieldMix):
    token = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.token
