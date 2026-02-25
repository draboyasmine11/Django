from django.shortcuts import render
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import Student, Teacher, Course, Grade, Attendance

def dashboard(request):
    # Statistiques générales
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_grades = Grade.objects.count()
    
    # Statistiques par statut
    active_students = Student.objects.filter(status='active').count()
    inactive_students = Student.objects.filter(status='inactive').count()
    graduated_students = Student.objects.filter(status='graduated').count()
    
    active_teachers = Teacher.objects.filter(status='active').count()
    inactive_teachers = Teacher.objects.filter(status='inactive').count()
    
    # Statistiques par classe
    students_by_class = Student.objects.values('class_name').annotate(count=Count('id')).order_by('-count')[:10]
    
    # Statistiques par matière
    teachers_by_subject = Teacher.objects.values('subject').annotate(count=Count('id')).order_by('-count')[:10]
    
    # Statistiques des notes
    avg_grades_by_course = Grade.objects.values('course__name').annotate(
        avg_grade=Avg('grade_value'),
        count=Count('id')
    ).order_by('-avg_grade')[:10]
    
    # Statistiques de présence
    today = timezone.now().date()
    attendance_today = Attendance.objects.filter(date=today).count()
    present_today = Attendance.objects.filter(date=today, status='present').count()
    absent_today = Attendance.objects.filter(date=today, status='absent').count()
    
    # Tendances (30 derniers jours)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_enrollments = Student.objects.filter(enrollment_date__gte=thirty_days_ago).count()
    recent_grades = Grade.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Top performers
    top_students = Grade.objects.values('student__first_name', 'student__last_name').annotate(
        avg_grade=Avg('grade_value')
    ).order_by('-avg_grade')[:10]
    
    # Dernières activités
    recent_grades_list = Grade.objects.select_related('student', 'course').order_by('-created_at')[:5]
    recent_attendance = Attendance.objects.select_related('student', 'course').order_by('-date')[:5]
    
    context = {
        # Statistiques générales
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_grades': total_grades,
        
        # Statistiques par statut
        'active_students': active_students,
        'inactive_students': inactive_students,
        'graduated_students': graduated_students,
        'active_teachers': active_teachers,
        'inactive_teachers': inactive_teachers,
        
        # Statistiques par classe et matière
        'students_by_class': students_by_class,
        'teachers_by_subject': teachers_by_subject,
        
        # Statistiques des notes
        'avg_grades_by_course': avg_grades_by_course,
        
        # Statistiques de présence
        'attendance_today': attendance_today,
        'present_today': present_today,
        'absent_today': absent_today,
        
        # Tendances
        'recent_enrollments': recent_enrollments,
        'recent_grades': recent_grades,
        
        # Top performers
        'top_students': top_students,
        
        # Dernières activités
        'recent_grades_list': recent_grades_list,
        'recent_attendance': recent_attendance,
    }
    
    return render(request, 'school/dashboard.html', context)

def statistics_detailed(request):
    # Statistiques détaillées avec graphiques
    from django.db.models import F, ExpressionWrapper, FloatField
    
    # Distribution des âges
    age_stats = {}
    for age in range(10, 26, 2):  # 10-12, 12-14, etc.
        age_min = age
        age_max = age + 2
        count = Student.objects.filter(
            date_of_birth__year__lte=timezone.now().year - age_min,
            date_of_birth__year__gt=timezone.now().year - age_max
        ).count()
        age_stats[f'{age}-{age_max} ans'] = count
    
    # Distribution des notes
    grade_distribution = {
        'Excellent (16-20)': Grade.objects.filter(grade_value__gte=16).count(),
        'Très Bien (14-16)': Grade.objects.filter(grade_value__gte=14, grade_value__lt=16).count(),
        'Bien (12-14)': Grade.objects.filter(grade_value__gte=12, grade_value__lt=14).count(),
        'Assez Bien (10-12)': Grade.objects.filter(grade_value__gte=10, grade_value__lt=12).count(),
        'Passable (8-10)': Grade.objects.filter(grade_value__gte=8, grade_value__lt=10).count(),
        'Insuffisant (<8)': Grade.objects.filter(grade_value__lt=8).count(),
    }
    
    # Taux de présence par mois
    attendance_rate = {}
    for i in range(6):
        month_start = timezone.now() - timedelta(days=30*i)
        month_end = timezone.now() - timedelta(days=30*(i-1)) if i > 0 else timezone.now()
        
        total_attendance = Attendance.objects.filter(date__range=[month_start.date(), month_end.date()]).count()
        present_attendance = Attendance.objects.filter(
            date__range=[month_start.date(), month_end.date()],
            status='present'
        ).count()
        
        if total_attendance > 0:
            rate = (present_attendance / total_attendance) * 100
        else:
            rate = 0
            
        attendance_rate[month_start.strftime('%B')] = round(rate, 1)
    
    context = {
        'age_stats': age_stats,
        'grade_distribution': grade_distribution,
        'attendance_rate': attendance_rate,
    }
    
    return render(request, 'school/statistics_detailed.html', context)
