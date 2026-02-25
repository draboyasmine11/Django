import django_filters
from django.db import models
from .models import Student, Teacher, Course, Grade, Attendance

class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    class_name = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Student.STATUS_CHOICES)
    gender = django_filters.ChoiceFilter(choices=Student.GENDER_CHOICES)
    age_min = django_filters.NumberFilter(method='filter_by_age_min')
    age_max = django_filters.NumberFilter(method='filter_by_age_max')
    enrollment_date_from = django_filters.DateFilter(field_name='enrollment_date', lookup_expr='gte')
    enrollment_date_to = django_filters.DateFilter(field_name='enrollment_date', lookup_expr='lte')

    class Meta:
        model = Student
        fields = ['class_name', 'status', 'gender']

    def filter_by_name(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(first_name__icontains=value) | 
                models.Q(last_name__icontains=value)
            )
        return queryset

    def filter_by_age_min(self, queryset, name, value):
        if value:
            from datetime import date
            max_birth_date = date.today().replace(year=date.today().year - value)
            return queryset.filter(date_of_birth__lte=max_birth_date)
        return queryset

    def filter_by_age_max(self, queryset, name, value):
        if value:
            from datetime import date
            min_birth_date = date.today().replace(year=date.today().year - value)
            return queryset.filter(date_of_birth__gte=min_birth_date)
        return queryset

class TeacherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_by_name')
    subject = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Teacher.STATUS_CHOICES)
    gender = django_filters.ChoiceFilter(choices=Teacher.GENDER_CHOICES)
    experience_min = django_filters.NumberFilter(field_name='experience_years', lookup_expr='gte')
    salary_min = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')
    hire_date_from = django_filters.DateFilter(field_name='hire_date', lookup_expr='gte')
    hire_date_to = django_filters.DateFilter(field_name='hire_date', lookup_expr='lte')

    class Meta:
        model = Teacher
        fields = ['subject', 'status', 'gender']

    def filter_by_name(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(first_name__icontains=value) | 
                models.Q(last_name__icontains=value)
            )
        return queryset

class CourseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    teacher = django_filters.CharFilter(method='filter_by_teacher')
    course_grade = django_filters.CharFilter(lookup_expr='icontains')
    max_students_min = django_filters.NumberFilter(field_name='max_students', lookup_expr='gte')

    class Meta:
        model = Course
        fields = ['name', 'code', 'course_grade']

    def filter_by_teacher(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(teacher__first_name__icontains=value) | 
                models.Q(teacher__last_name__icontains=value)
            )
        return queryset

class GradeFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(method='filter_by_student')
    course = django_filters.CharFilter(method='filter_by_course')
    teacher = django_filters.CharFilter(method='filter_by_teacher')
    grade_min = django_filters.NumberFilter(field_name='grade_value', lookup_expr='gte')
    grade_max = django_filters.NumberFilter(field_name='grade_value', lookup_expr='lte')
    exam_date_from = django_filters.DateFilter(field_name='exam_date', lookup_expr='gte')
    exam_date_to = django_filters.DateFilter(field_name='exam_date', lookup_expr='lte')

    class Meta:
        model = Grade
        fields = []

    def filter_by_student(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(student__first_name__icontains=value) | 
                models.Q(student__last_name__icontains=value)
            )
        return queryset

    def filter_by_course(self, queryset, name, value):
        if value:
            return queryset.filter(course__name__icontains=value)
        return queryset

    def filter_by_teacher(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(teacher__first_name__icontains=value) | 
                models.Q(teacher__last_name__icontains=value)
            )
        return queryset

class AttendanceFilter(django_filters.FilterSet):
    student = django_filters.CharFilter(method='filter_by_student')
    course = django_filters.CharFilter(method='filter_by_course')
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Attendance
        fields = ['status']

    def filter_by_student(self, queryset, name, value):
        if value:
            return queryset.filter(
                models.Q(student__first_name__icontains=value) | 
                models.Q(student__last_name__icontains=value)
            )
        return queryset

    def filter_by_course(self, queryset, name, value):
        if value:
            return queryset.filter(course__name__icontains=value)
        return queryset
