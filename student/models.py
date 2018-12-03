from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime
from django.urls import reverse


class MyUser(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)


class Student(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    student_no = models.CharField(unique=True, max_length=9, help_text="student number")
    student_name = models.CharField(max_length=50, help_text="student name")
    student_surname = models.CharField(max_length=50, help_text="student surname")

    class Meta:
        permissions = (("can_upload_photo", "Upload Photo Permission"),)

    def __str__(self):
        return self.student_no


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    teacher_no = models.CharField(unique=True, max_length=9, help_text="teacher id")
    teacher_name = models.CharField(max_length=50, help_text="teacher name")
    teacher_surname = models.CharField(max_length=50, help_text="teacher surname")

    def __str__(self):
        return f"{self.teacher_no} : {self.teacher_name} {self.teacher_surname}"


class StudentCourse(models.Model):
    student_table = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    lecture_table = models.ForeignKey('Lecture', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.student_table)


class CourseTeacher(models.Model):

    lecture_table = models.ForeignKey('Lecture', on_delete=models.SET_NULL, null=True, blank=True)
    teacher_no = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('lecture-detail', args=[str(self.lecture_table)])


class Lecture(models.Model):
    CHOICES = (
        ('MON.', 'Monday'),
        ('TUES.', 'Tuesday'),
        ('WED.', 'Wednesday'),
        ('THU.', 'Thursday'),
        ('FRI.', 'Friday'),
    )

    lecture_crn = models.CharField(primary_key=True, max_length=5, help_text="section crn")
    lecture_day = models.CharField(choices=CHOICES, max_length=10)
    course_id = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    teacher_no = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.TimeField(default=datetime.time(8, 30), null=False, blank=False)
    end_time = models.TimeField(default=datetime.time(11, 30), null=False, blank=False)

    def __str__(self):
        return self.lecture_crn

    def get_absolute_url(self):
        return reverse('lecture-detail', args=[str(self.lecture_crn)])


class Course(models.Model):

    course_id = models.AutoField(primary_key=True, help_text="Course id")
    course_name = models.CharField(max_length=50, help_text="Course name")

    def __str__(self):
        return self.course_name

    def get_absolute_url(self):
        return reverse('lecture-detail', args=[str(self.course_id)])


class Attendance(models.Model):
    student_id = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    lecture_crn = models.ForeignKey('Lecture', on_delete=models.SET_NULL, null=True, blank=True)
    date_attended = models.DateField("date")
    inout = models.BooleanField("input")
