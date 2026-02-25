from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Student, Teacher, Course, Grade, Attendance
from .forms import StudentForm, TeacherForm, CourseForm, GradeForm, AttendanceForm
from .filters import StudentFilter, TeacherFilter, CourseFilter, GradeFilter, AttendanceFilter
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

@login_required
def student_list_advanced(request):
    students = Student.objects.all()
    student_filter = StudentFilter(request.GET, queryset=students)
    
    paginator = Paginator(student_filter.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter': student_filter,
        'page_obj': page_obj,
        'students': page_obj,
    }
    return render(request, 'school/student_list_advanced.html', context)

@login_required
def teacher_list_advanced(request):
    teachers = Teacher.objects.all()
    teacher_filter = TeacherFilter(request.GET, queryset=teachers)
    
    paginator = Paginator(teacher_filter.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter': teacher_filter,
        'page_obj': page_obj,
        'teachers': page_obj,
    }
    return render(request, 'school/teacher_list_advanced.html', context)

@login_required
def course_list(request):
    courses = Course.objects.all()
    course_filter = CourseFilter(request.GET, queryset=courses)
    
    paginator = Paginator(course_filter.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter': course_filter,
        'page_obj': page_obj,
        'courses': page_obj,
    }
    return render(request, 'school/course_list.html', context)

@login_required
def grade_list(request):
    grades = Grade.objects.all()
    grade_filter = GradeFilter(request.GET, queryset=grades)
    
    paginator = Paginator(grade_filter.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter': grade_filter,
        'page_obj': page_obj,
        'grades': page_obj,
    }
    return render(request, 'school/grade_list.html', context)

@login_required
def attendance_list(request):
    attendances = Attendance.objects.all()
    attendance_filter = AttendanceFilter(request.GET, queryset=attendances)
    
    paginator = Paginator(attendance_filter.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'filter': attendance_filter,
        'page_obj': page_obj,
        'attendances': page_obj,
    }
    return render(request, 'school/attendance_list.html', context)

# Vues pour les formulaires CRUD
@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours créé avec succès!')
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'school/course_form.html', {'form': form, 'title': 'Ajouter un cours'})

@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours modifié avec succès!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'school/course_form.html', {'form': form, 'title': 'Modifier un cours'})

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Cours supprimé avec succès!')
        return redirect('course_list')
    return render(request, 'school/course_confirm_delete.html', {'course': course})

@login_required
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note ajoutée avec succès!')
            return redirect('grade_list')
    else:
        form = GradeForm()
    return render(request, 'school/grade_form.html', {'form': form, 'title': 'Ajouter une note'})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Présence enregistrée avec succès!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'school/attendance_form.html', {'form': form, 'title': 'Enregistrer la présence'})

# Fonctions d'export
@login_required
def export_students_excel(request):
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=students.xlsx'
    
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Étudiants'
    
    # En-têtes
    headers = ['Nom', 'Prénom', 'Email', 'Classe', 'Statut', 'Date d\'inscription', 'Téléphone']
    worksheet.append(headers)
    
    # Données
    students = Student.objects.all()
    for student in students:
        row = [
            student.last_name,
            student.first_name,
            student.email,
            student.class_name,
            student.get_status_display(),
            student.enrollment_date.strftime('%d/%m/%Y'),
            student.phone or ''
        ]
        worksheet.append(row)
    
    workbook.save(response)
    return response

@login_required
def export_students_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=students.pdf'
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Liste des Étudiants")
    
    # En-têtes de tableau
    p.setFont("Helvetica-Bold", 12)
    y_position = 700
    headers = ['Nom', 'Prénom', 'Email', 'Classe']
    x_positions = [50, 150, 250, 400]
    
    for i, header in enumerate(headers):
        p.drawString(x_positions[i], y_position, header)
    
    # Données
    p.setFont("Helvetica", 10)
    y_position -= 30
    students = Student.objects.all()[:20]  # Limite à 20 étudiants pour le PDF
    
    for student in students:
        p.drawString(50, y_position, student.last_name)
        p.drawString(150, y_position, student.first_name)
        p.drawString(250, y_position, student.email)
        p.drawString(400, y_position, student.class_name)
        y_position -= 20
        
        if y_position < 50:  # Nouvelle page si nécessaire
            p.showPage()
            y_position = 700
    
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()
    
    return response
