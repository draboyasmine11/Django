from django import forms
from .models import Student, Teacher, Course, Grade, Attendance

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'class_name', 'gender', 
                 'phone', 'address', 'photo', 'status', 'emergency_contact', 'emergency_phone', 'medical_info']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_info': forms.Textarea(attrs={'rows': 3}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'gender', 
                 'address', 'photo', 'status', 'salary', 'qualification', 'experience_years']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'credits', 'teacher', 'course_grade', 'schedule', 'max_students']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'schedule': forms.Textarea(attrs={'rows': 2}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'teacher', 'grade_value', 'max_grade', 'exam_date', 'comments']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
