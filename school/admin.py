from django.contrib import admin
from .models import Student, Teacher

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'grade', 'enrollment_date')
    list_filter = ('grade', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'enrollment_date'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'hire_date')
    list_filter = ('subject', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'hire_date'
