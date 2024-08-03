from django.contrib import admin
from content.models import Grade, Class, Unit, Question, Source

def name(obj): 
    return str(obj)

def number_of_questions(obj):
    return obj.count_questions()

def number_of_questions_unit(obj):
    return obj.questions.count()

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade_number']
    #fields = ['name', 'grade_number']

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'grade_number', number_of_questions]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'class_rel', number_of_questions_unit]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', name, 'unit', 'source']

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']