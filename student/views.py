from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from student.models import Student, StudentCourse, Lecture, Teacher, CourseTeacher, Course, Attendance
from django.views import generic
import datetime
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage


# Create your views here.


def index(request):
    context = {
        'deneme': 3,
    }

    return render(request, 'index.html', context=context)


def upload_image(request):
    if request.method == 'POST' and request.FILES['file']:

        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'student/image_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'student/image_upload.html')







