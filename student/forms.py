from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from student.models import MyUser


class ImageUploadForm(forms.Form):
    """Image upload form."""
    title = forms.CharField(max_length=50)
    image = forms.ImageField()


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user


class TeacherSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user

