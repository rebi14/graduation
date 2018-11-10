from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from student.forms import StudentSignUpForm, TeacherSignUpForm
from student.models import MyUser
# Create your views here.


class StudentSignUpView(CreateView):
    model = MyUser
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index.html')


class TeacherSignUpView(CreateView):
    model = MyUser
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index.html')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def index(request):

    return render(request, 'index.html')


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







