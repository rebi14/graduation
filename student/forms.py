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
