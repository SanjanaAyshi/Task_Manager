from django.contrib import admin
from .models import UserTaskAccount,UserAddress
# Register your models here.

admin.site.register(UserTaskAccount)
admin.site.register(UserAddress)