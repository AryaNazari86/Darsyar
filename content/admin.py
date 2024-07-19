from django.contrib import admin
from content.models import Grade, Class, Unit, Question, Source

def name(obj): 
    return str(obj)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade_number']
    #fields = ['name', 'grade_number']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade_number']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'class_rel']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', name, 'unit', 'source']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']