from django.urls import path
from . import views
from django.views.generic.edit import CreateView, UpdateView

from management.views import TutorialListView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/',views.StudentDeleteView.as_view(), name='student_delete'),
    
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/report/', views.attendance_report, name='attendance_report'),
    
    path('fees/', views.FeeListView.as_view(), name='fee_list'),
    path('fees/add/', views.FeeCreateView.as_view(), name='fee_add'),
    path('fees/<int:pk>/edit/', views.FeeCreateView.as_view(), name='fee_edit'),
    path('fees/<int:pk>/pay/', views.fee_payment, name='fee_payment'),
    path('fees/report/', views.fee_report, name='fee_report'),
    path('fees/<int:pk>/delete/',views.FeeDeleteView.as_view(), name= 'fee_delete'),
    path('fees/generate/', views.generate_fees, name='generate_fees'),
    path('export/fees/excel/', views.export_fees_excel, name='fee_export_excel'),
    
    path('lesson-plans/', views.LessonPlanListView.as_view(), name='lesson_plan_list'),
    path('lesson-plans/add/', views.LessonPlanCreateView.as_view(), name='lesson_plan_add'),
    path('lesson-plans/<int:pk>/', views.LessonPlanDetailView.as_view(), name='lesson_plan_detail'),
    path('lesson-plans/<int:pk>/edit/', views.LessonPlanUpdateView.as_view(), name='lesson_plan_edit'),
    path('lesson-plans/<int:pk>/delete/', views.LessonPlanDeleteView.as_view(), name='lesson_plan_delete'),
    
    path('reports/', views.generate_report, name='generate_report'),
    
    path('export/students/', views.export_students_csv, name='export_students_csv'),
    path('export/attendance/', views.export_attendance_csv, name='export_attendance'),
    path('export/attendance/excel/', views.export_attendance_excel, name='export_attendance_excel'),
    path('export/fees/excel/', views.export_fees_excel, name='export_fees_excel'),
    path('tutorials/', views.student_tutorial_list, name='tutorial_list'),
    path('tutorials/<int:pk>/', views.student_tutorial_detail, name='tutorial_detail'),
    path('export/attendance/report/excel/', views.export_attendance_report_excel, name='export_attendance_report_excel'),

# Admin/teacher tutorial management
    path('manage/tutorials/', views.TutorialListView.as_view(), name='tutorial_list_admin'),
    path('manage/tutorials/add/', views.TutorialCreateView.as_view(), name='tutorial_add'),
    path('manage/tutorials/<int:pk>/edit/', views.TutorialUpdateView.as_view(), name='tutorial_edit'),
    path('manage/tutorials/<int:pk>/delete/', views.TutorialDeleteView.as_view(), name='tutorial_delete'),
    path('manage/tutorials/<int:pk>/progress/', views.TutorialProgressView.as_view(), name='tutorial_progress'),

    path('after-login-redirect/', views.after_login_redirect, name='after_login_redirect'),
    
    path('classes/add/', views.ClassCreateView.as_view(), name='class_add'),
    
    # Grade URLs
    path('grades/', views.GradeListView.as_view(), name='grade_list'),
    path('grades/add/', views.GradeCreateView.as_view(), name='grade_add'),
    path('grades/bulk/', views.bulk_grade_entry, name='grade_bulk'),
    path('grades/<int:pk>/edit/', views.GradeUpdateView.as_view(), name='grade_edit'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade_delete'),
    path('student/<int:pk>/transcript/', views.student_transcript, name='student_transcript'),
    path('grades/<int:pk>/', views.GradeDetailView.as_view(), name='grade_detail'),
    

    # Timetable URLs
    path('timetable/', views.TimetableEntryListView.as_view(), name='timetable_list'),
    path('timetable/add/', views.TimetableEntryCreateView.as_view(), name='timetable_add'),
    path('timetable/<int:pk>/edit/', views.TimetableEntryUpdateView.as_view(), name='timetable_edit'),
    path('timetable/<int:pk>/delete/', views.TimetableEntryDeleteView.as_view(), name='timetable_delete'),
    path('timetable/class/<int:class_id>/', views.view_class_timetable, name='timetable_view'),
    path('timetable/copy/', views.copy_timetable, name='timetable_copy'),
    path('my-timetable/', views.my_timetable, name='my_timetable'),

# Day URLs - Add these to your urlpatterns
    path('days/', views.DayListView.as_view(), name='day_list'),
    path('days/add/', views.DayCreateView.as_view(), name='day_add'),
    path('days/<int:pk>/edit/', views.DayUpdateView.as_view(), name='day_edit'),
    path('days/<int:pk>/delete/', views.DayDeleteView.as_view(), name='day_delete'),

    # Period URLs
    path('periods/', views.PeriodListView.as_view(), name='period_list'),
    path('periods/add/', views.PeriodCreateView.as_view(), name='period_add'),
    path('periods/<int:pk>/edit/', views.PeriodUpdateView.as_view(), name='period_edit'),
    path('periods/<int:pk>/delete/', views.PeriodDeleteView.as_view(), name='period_delete'),
]