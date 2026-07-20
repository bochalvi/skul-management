from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'Gender', 'Admission_Number', 'is_active']
    list_filter = ['is_active', 'Gender']
    search_fields = ['First_Name', 'Last_Name', 'Admission_Number']  # ✅ Fixed
    list_per_page = 20
    
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'attendance_date', 'status', 'check_in_time', 'check_out_time']
    list_filter = ['attendance_date', 'status']
    search_fields = ['student_First_Name', 'student_Last_Name']  # ✅ Fixed (use single underscore)
    list_per_page = 25
    
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_type', 'amount_due', 'amount_paid', 'due_date', 'status']
    list_filter = ['status', 'payment_method', 'due_date']
    search_fields = ['student_First_Name', 'studentLast_Name', 'student_Admission_Number']  # ✅ Fixed
    list_per_page = 20
    
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'frequency', 'is_active']
    list_filter = ['frequency', 'is_active']
    search_fields = ['name']
    list_per_page = 20
    
class LessonPlanAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'class_assigned', 'subject', 'topic', 'date', 'status']
    list_filter = ['subject', 'status', 'date']
    search_fields = ['teacher_username', 'teacherfirst_name', 'teacher_last_name', 'subject', 'topic']
    list_per_page = 20
    
class TutorialAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'grade_level', 'is_published', 'created_at']
    list_filter = ['subject', 'is_published', 'created_at']
    search_fields = ['title', 'subject', 'description']
    list_per_page = 20
    
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'grade_level', 'academic_year', 'teacher']
    list_filter = ['grade_level', 'academic_year']
    search_fields = ['name', 'teacher_username', 'teacherfirst_name', 'teacher_last_name']
    list_per_page = 20

class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'grade', 'exam_type', 'recorded_at']
    list_filter = ['subject', 'exam_type', 'recorded_at']
    search_fields = ['student_First_Name', 'student_Last_Name', 'subject']
    list_per_page = 20

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'title']
    list_per_page = 20

class StudentTutorialProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'tutorial', 'completed', 'completed_at']
    list_filter = ['completed', 'completed_at']
    search_fields = ['student_First_Name', 'studentLast_Name', 'tutorial_title']
    list_per_page = 20

# Register all models
admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Fee, FeeAdmin)
admin.site.register(FeeType, FeeTypeAdmin)
admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(LessonPlan, LessonPlanAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(StudentTutorialProgress, StudentTutorialProgressAdmin)

# Customize admin site
admin.site.site_header = "School Management System"
admin.site.site_title = "School Admin Portal"
admin.site.index_title = "Welcome to School Management System"