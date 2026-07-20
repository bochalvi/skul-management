from django import forms
from .models import Student, Attendance, Grade, Fee, LessonPlan, Tutorial, Class,FeeType,Enrollment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Attendance, Grade,Fee,LessonPlan,Tutorial
from django.core.exceptions import ValidationError
from datetime import date
from .models import TimetableEntry, Period, Day



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email address already in use.")
        return email
    
class StudentRegistrationForm(forms.ModelForm):
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']
        
    )
    enrollment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        initial=date.today
    )
    
    class Meta:
        model = Student
        fields = '__all__'
    
   
        
        

class AttendanceForm(forms.ModelForm):
    attendance_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        initial=date.today,
    )

    class Meta:
        model = Attendance
        fields = '__all__'
        widgets = {
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
# ...existing code...
        
class BulkAttendanceForm(forms.Form):
    attendance_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        initial=date.today
    )
    class_group = forms.ModelChoiceField(queryset=None, required=False)
    
    def __init__(self, *args, **kwargs):
        from .models import Class
        super(BulkAttendanceForm, self).__init__(*args, **kwargs)
        self.fields['class_group'].queryset = Class.objects.all()
        
class FeeForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        required=True
    )
    
    class Meta:
        model = Fee
        fields = [
            'student',
            'fee_type',
            'amount_due',
            'amount_paid',
            'due_date',
            'paid_date',
            'payment_method',
            'transaction_id',
            'status',
            'notes'
        ]
        widgets = {
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        
class LessonPlanForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        initial=date.today
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M']
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M']
    )
    
    class Meta:
        model = LessonPlan
        fields = [
            'teacher',
            'class_assigned',
            'subject',
            'grade_level',
            'topic',
            'objectives',
            'materials',
            'activities',
            'assessment_methods',
            'homework',
            'duration',
            'day_of_week',
            'date',
            'start_time',
            'end_time',
            'status'
        ]
        widgets = {
            'objectives': forms.Textarea(attrs={'rows': 4}),
            'materials': forms.Textarea(attrs={'rows': 3}),
            'activities': forms.Textarea(attrs={'rows': 6}),
            'assessment_methods': forms.Textarea(attrs={'rows': 3}),
            'homework': forms.Textarea(attrs={'rows': 3}),
        }
        
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'class_assigned', 'subject', 'grade', 'exam_type', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'recorded_at': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Limit students to active ones
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
        # Add a default value for recorded_by in the view

class BulkGradeForm(forms.Form):
    """Form for entering grades for multiple students at once"""
    class_assigned = forms.ModelChoiceField(queryset=Class.objects.all(), required=True)
    subject = forms.CharField(max_length=100, required=True)
    exam_type = forms.CharField(max_length=50, required=True)
    exam_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        
class ReportFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        required=False
    )
    student = forms.ModelChoiceField(queryset=Student.objects.all(), required=False)
    class_group = forms.ModelChoiceField(queryset=None, required=False)
    
    def __init__(self, *args, **kwargs):
        from .models import Class
        super(ReportFilterForm, self).__init__(*args, **kwargs)
        self.fields['class_group'].queryset = Class.objects.all()
        
class TutorialForm(forms.ModelForm):
    class Meta:
        model = Tutorial
        fields = ['title', 'description', 'subject', 'grade_level', 'content', 'video_url', 'attachment', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
        
class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ['class_assigned', 'day', 'period', 'subject', 'teacher', 'room', 'is_break', 'break_name']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'room': forms.TextInput(attrs={'class': 'form-control'}),
            'break_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['class_assigned'].queryset = Class.objects.all()
        self.fields['day'].queryset = Day.objects.filter(is_active=True)
        self.fields['period'].queryset = Period.objects.all()
        self.fields['teacher'].queryset = User.objects.filter(groups__name='Teachers')

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['period_number', 'start_time', 'end_time', 'name']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['day_number', 'name', 'is_active']

class BulkTimetableForm(forms.Form):
    """Form for copying timetable from one class to another"""
    source_class = forms.ModelChoiceField(queryset=Class.objects.all(), label="Copy From")
    target_class = forms.ModelChoiceField(queryset=Class.objects.all(), label="Copy To")
    academic_year = forms.CharField(max_length=20, initial='2024')
    term = forms.CharField(max_length=20, initial='Term 1')