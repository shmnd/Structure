from django.contrib import admin
from .models import User,GeneratedAccessToken
# Register your models here.
admin.site.register(User)
admin.site.register(GeneratedAccessToken)
