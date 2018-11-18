from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from student.models import MyUser, Student, Teacher


class ImageUploadForm(forms.Form):
    """Image upload form."""
    title = forms.CharField(max_length=50)
    image = forms.ImageField()


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

