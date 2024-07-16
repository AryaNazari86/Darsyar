from django.contrib import admin
from user.models import User

def name(obj): 
    return str(obj)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', name, 'grade']
    