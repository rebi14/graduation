from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from student.models import MyUser, Student, Teacher, Lecture, StudentCourse
from django.forms import ModelForm
from django.forms import *

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('username', 'first_name', 'last_name')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True

        if commit:
            user.save()

            student = Student.objects.create(user=user, student_no=user.username, student_name=user.first_name,
                                             student_surname=user.last_name)
            student.save()

        return user


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ('username', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()

            teacher = Teacher.objects.create(user=user, teacher_no=user.username, teacher_name=user.first_name,
                                             teacher_surname=user.last_name)
            teacher.save()

        return user


class EnrollLectureForm(ModelForm):

    class Meta:

        model = StudentCourse
        fields = ('lecture_table', )
        labels = {
            'lecture_table': 'Lecture CRN  ',
        }
        # help_texts = {
        #     'lecture_table': '',
        # }
        widgets = {
            'lecture_table': Select(attrs={'class': 'form-control'})
            }


class CreateLectureForm(ModelForm):

    class Meta:
        model = Lecture
        exclude = ('teacher_no',)
        labels = {
            'course_id': 'Course Code',
            'lecture_crn': 'Lecture CRN  ',
            'lecture_day': 'Lecture Day',
            'teacher_no': 'Course Teacher',

        }
        help_texts = {
            'lecture_crn': '',
        }
        widgets = {
            'course_id': Select(attrs={'class': 'form-control'}),
            'lecture_crn': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CRN'}),
            'lecture_day': Select(attrs={'class': 'form-control'}),
            'teacher_no': Select(attrs={'class': 'form-control'}),
            'start_time': DateTimeInput(attrs={'class': 'form-control'}),
            'end_time': DateTimeInput(attrs={'class': 'form-control'})
        }
