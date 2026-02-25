from django.contrib import admin
from .models import Student, Teacher, Course, Grade, Attendance, StudentTeacher

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'class_name', 'status', 'enrollment_date')
    list_filter = ('class_name', 'status', 'gender', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'email', 'class_name')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'enrollment_date'
    readonly_fields = ('age',)
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Âge'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject', 'status', 'hire_date')
    list_filter = ('subject', 'status', 'gender', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    ordering = ('last_name', 'first_name')
    date_hierarchy = 'hire_date'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'teacher', 'course_grade', 'max_students', 'enrolled_count')
    list_filter = ('course_grade', 'teacher')
    search_fields = ('name', 'code', 'teacher__first_name', 'teacher__last_name')
    ordering = ('code',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'teacher', 'grade_value', 'max_grade', 'exam_date')
    list_filter = ('course', 'teacher', 'exam_date')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    ordering = ('-exam_date',)
    date_hierarchy = 'exam_date'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    list_filter = ('status', 'course', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    ordering = ('-date',)
    date_hierarchy = 'date'

@admin.register(StudentTeacher)
class StudentTeacherAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'course', 'enrollment_date', 'grade')
    list_filter = ('course', 'enrollment_date')
    search_fields = ('student__first_name', 'student__last_name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('-enrollment_date',)
