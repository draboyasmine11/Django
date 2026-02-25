from django.urls import path
from . import views
from . import dashboard_views
from . import views_advanced

from django.urls import include
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    
    # Dashboard
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    
    # Étudiants (ancien et avancé)
    path('students/', views.student_list, name='student_list'),
    path('students/advanced/', views_advanced.student_list_advanced, name='student_list_advanced'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('students/export/excel/', views_advanced.export_students_excel, name='export_students_excel'),
    path('students/export/pdf/', views_advanced.export_students_pdf, name='export_students_pdf'),
    
    # Enseignants (ancien et avancé)
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/advanced/', views_advanced.teacher_list_advanced, name='teacher_list_advanced'),
    path('teachers/add/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:pk>/edit/', views.teacher_update, name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
    
    # Cours
    path('courses/', views_advanced.course_list, name='course_list'),
    path('courses/add/', views_advanced.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views_advanced.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views_advanced.course_delete, name='course_delete'),
    
    # Notes
    path('grades/', views_advanced.grade_list, name='grade_list'),
    path('grades/add/', views_advanced.grade_create, name='grade_create'),
    
    # Présences
    path('attendance/', views_advanced.attendance_list, name='attendance_list'),
    path('attendance/add/', views_advanced.attendance_create, name='attendance_create'),
]
