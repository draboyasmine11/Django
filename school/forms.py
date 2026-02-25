from django import forms
from .models import Student, Teacher

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'grade']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
