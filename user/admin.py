from django.contrib import admin
from user.models import User, UserQuestionRel

def name(obj): 
    return str(obj)

def score(obj):
    return obj.score()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', name, 'grade', score]
    
@admin.register(UserQuestionRel)
class UserQuestionRelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question']
    