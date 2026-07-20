from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


# Create your models here.
def current_date():
    return date.today
class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    Admission_Number = models.CharField(max_length=20, unique=True)
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    Address = models.TextField()
    Contact_Number = models.CharField(max_length=15)    
    Parent_Guardian_Name = models.CharField(max_length=100)
    Parent_Guardian_Contact = models.CharField(max_length=15)
    Parent_Guardian_Email = models.EmailField()
    Enrollment_Date = models.DateField()
    Photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['Last_Name', 'First_Name']
        
    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.Admission_Number})"
    
    @property
    def full_name(self):
        return f"{self.First_Name} {self.Last_Name}"
    
    def get_age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    
class Class(models.Model):
    name = models.CharField(max_length=50)
    grade_level = models.CharField( max_length=50)
    academic_year = models.CharField(max_length=20)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Teachers'})
    students = models.ManyToManyField(Student, through='Enrollment')
    
    def __str__(self):
        return f"{self.name} - {self.grade_level} ({self.academic_year})"
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'class_enrolled')
class Day(models.Model):
    calendar_date = models.DateField(unique=True)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
    ]
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    attendance_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ('student','attendance_date')
        ordering = ['-attendance_date','student']
        
    def __str__(self):
        return f"{self.student} - {self.attendance_date}: {self.get_status_display()}"
    
class FeeType(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    frequency = models.CharField(max_length=50, choices=[('One-time', 'One-time'), ('Monthly', 'Monthly'), ('Termly', 'Termly'), ('Yearly', 'Yearly')])
    description = models.TextField(blank=True)  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.amount} ({self.frequency})"
    
class Fee(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Unpaid', 'Unpaid'),
        ('partially paid', 'Partially Paid'),
        ('Overdue', 'Overdue'),
        ('Cancelled', 'Cancelled'),
        ('Refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('Cheque', 'Cheque'),
        ('Mobile Payment', 'Mobile Payment'),
        ('Other', 'Other'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.SET_NULL, null=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Unpaid')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-due_date', 'student__Last_Name', 'student__First_Name']
        
    def __str__(self):
        return f"{self.student.full_name} - {self.fee_type.name} - {self.amount_due} - {self.get_status_display()}"
    
    @property
    def balance(self):
        return self.amount_due - self.amount_paid
    
    @property
    def is_overdue(self):
        from datetime import date
        return self.status != 'Paid' and self.due_date < date.today()

    
class LessonPlan(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Teachers'})
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=50)
    topic = models.CharField(max_length=200)
    objectives = models.TextField()
    materials = models.TextField(blank=True)
    activities = models.TextField(blank=True)
    assessment_methods = models.TextField(blank=True)
    homework = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", validators=[MinValueValidator(1)])
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Planned', 'Planned'),('Draft','Draft'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Planned')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'start_time']
        
    def __str__(self):
        return f"{self.subject} - {self.topic} ({self.date})"
    
    
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    grade = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    exam_type = models.CharField(max_length=50, choices=[('Midterm', 'Midterm'), ('Final', 'Final'), ('Quiz', 'Quiz'), ('Assignment', 'Assignment')])
    comments = models.TextField(blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Teachers'})
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'class_assigned', 'subject')
        ordering = ['-recorded_at', 'student__Last_Name', 'student__First_Name']
        
    def __str__(self):
        return f"{self.student.full_name} - {self.subject} - {self.grade}"
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.title}"
    
class Tutorial(models.Model):
    """Learning material for students"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20, blank=True)
    content = models.TextField(help_text="HTML or Markdown content")
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo link")
    attachment = models.FileField(upload_to='tutorials/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tutorials_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def _str_(self):
        return self.title

class StudentTutorialProgress(models.Model):
    """Tracks which tutorials a student has completed"""
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='tutorial_progress')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='student_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_viewed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'tutorial']

    def _str_(self):
        return f"{self.student} - {self.tutorial} - {'Completed' if self.completed else 'Incomplete'}"   
    
class Period(models.Model):
    """Class periods/times"""
    period_number = models.IntegerField(unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    name = models.CharField(max_length=50, blank=True)  # e.g., "1st Period", "Morning Session"
    
    class Meta:
        ordering = ['period_number']
    
    def _str_(self):
        return f"Period {self.period_number}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class Day(models.Model):
    """Days of the week"""
    DAYS = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
    day_number = models.IntegerField(choices=DAYS, unique=True,null=True, blank=True)
    name = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day_number']
    
    def _str_(self):
        return self.name

class TimetableEntry(models.Model):
    """Individual timetable entry for a class, day, and period"""
    class_assigned = models.ForeignKey('Class', on_delete=models.CASCADE, related_name='timetable_entries')
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'Teachers'})
    room = models.CharField(max_length=50, blank=True)
    is_break = models.BooleanField(default=False)
    break_name = models.CharField(max_length=100, blank=True)
    academic_year = models.CharField(max_length=20, default='2024')
    term = models.CharField(max_length=20, default='Term 1')
    
    class Meta:
        unique_together = ['class_assigned', 'day', 'period', 'academic_year', 'term']
        ordering = ['class_assigned__name', 'day__day_number', 'period__period_number']
    
    def _str_(self):
        return f"{self.class_assigned.name} - {self.day.name} - Period {self.period.period_number}: {self.subject}"