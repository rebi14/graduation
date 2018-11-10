from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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
        return f"{self.teacher_name} {self.teacher_surname}"


class StudentCourse(models.Model):
    student_no = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    course_id = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.student_no


class CourseTeacher(models.Model):

    course_id = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    teacher_no = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)


class Lecture(models.Model):
    lecture_crn = models.CharField(primary_key=True, max_length=5, help_text="section crn")
    lecture_day = models.DateTimeField()
    course_id = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    teacher_no = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.lecture_crn


class Course(models.Model):

    course_id = models.AutoField(primary_key=True, help_text="Course id")
    course_name = models.CharField(max_length=50, help_text="Course name")

    def __str__(self):
        return self.course_name


class Attendance(models.Model):
    student_id = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    lecture_crn = models.ForeignKey('Lecture', on_delete=models.SET_NULL, null=True, blank=True)
    date_attended = models.DateField("date")
    inout = models.BooleanField("input")
