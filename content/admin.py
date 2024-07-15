from django.contrib import admin
from content.models import Grade, Class, Question

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade_number']
    #fields = ['name', 'grade_number']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade_number']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'answer', 'class_rel']