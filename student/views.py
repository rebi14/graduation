from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from student.forms import StudentSignUpForm, TeacherSignUpForm, EnrollLectureForm
from student.models import *
from django.views import generic

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
#        login(self.request, user)
        return redirect('/')


class TeacherSignUpView(CreateView):
    model = MyUser
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        #login(self.request, user)
        return redirect('/')


class LectureEnrollmentView(CreateView):
    model = StudentCourse
    form_class = EnrollLectureForm
    template_name = 'student/enrolment.html'

    def get_object(self, queryset=None):
        obj, created = StudentCourse.objects.get_or_create(col_1=self.kwargs['value_1'], col_2=self.kwargs['value_2'])
        return obj


def enrolment(request):
    if request.method == 'POST':
        form = EnrollLectureForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            lec = Lecture.objects.get(lecture_crn=a.lecture_table.lecture_crn)
            stu = Student.objects.get(student_no=request.user.username)
            Lecture.objects.get(lecture_crn=a.lecture_table.lecture_crn)
            if StudentCourse.objects.filter(student_table=stu, lecture_table=lec).exists():
                return render(request, 'index.html')
            else:
                StudentCourse.objects.create(lecture_table=lec, student_table=stu)
                redirect('/')
    else:
        form = EnrollLectureForm()
    return render(request, 'student/enrolment.html', {'form': form})


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


class GetAllCourse(LoginRequiredMixin, generic.ListView):

    model = Lecture
    template_name = "student/all_lecture.html"

    def get_queryset(self):
        return Lecture.objects.all()


class GetStudentLecture(LoginRequiredMixin, generic.ListView):

    model = Lecture
    template_name = "student/student_course.html"
    # context_object_name = 'student_lecture_list'

    def get_queryset(self):
        #return Lecture.objects.select_related('course_id')

        return Lecture.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GetStudentLecture, self).get_context_data(**kwargs)
        context['student_courses'] = StudentCourse.objects.all()
        return context


class CourseCreate(LoginRequiredMixin, CreateView):



    pass
