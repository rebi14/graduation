import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from student.forms import StudentSignUpForm, TeacherSignUpForm, EnrollLectureForm, CreateLectureForm
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


class CreateLecture(LoginRequiredMixin, CreateView):

    model = Lecture
    template_name = "teacher/create_lecture.html"
    success_url = '/'
    form_class = CreateLectureForm

    def form_valid(self, form):
        teacher = Teacher.objects.get(teacher_no=self.request.user.username)
        form.instance.teacher_no = teacher
        return super().form_valid(form)

    # def get_absolute_url(self):
    #     return '/'


class GetTeacherLecture(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'teacher/teacher_lecture.html'

    def get_queryset(self):
        teacher = Teacher.objects.get(teacher_no=self.request.user.username)
        return Lecture.objects.filter(teacher_no=teacher)


class GetLectureStudentList(LoginRequiredMixin, ListView):
    model = StudentCourse
    template_name = 'teacher/lecture_detail.html'
    print("\n")
    print("\n")

    def get_queryset(self):
        print(self.request.path)
        a = self.request.path
        print(type(a))
        crn = re.findall(r'[0-9].*', a)
        lec = Lecture.objects.get(lecture_crn=crn[0])
        return StudentCourse.objects.filter(lecture_table=lec)

    # def get_queryset(self):
    #     return StudentCourse.objects.raw("SELECT student_table_id FROM student_studentcourse where lecture_table_id=10000;")
    # def get_queryset(self):
    #     return StudentCourse.objects.filter()

    # template_name = 'teacher/lecture_detail.html'

    # def get_queryset(self):
    #     teacher = Teacher.objects.get(teacher_no=self.request.user.username)
    #     lecture = Lecture.objects.filter(teacher_no=teacher)
    #
    #
    #     crn = re.findall(r'[0-9].*', )
    #
    #     print(lecture[0].lecture_crn)
    #     print("\n")
    #     print(StudentCourse.objects.filter(lecture_table=lecture[0]))
    #     print("\n")
    #     print(lecture[0].get_absolute_url())
    #     print("\n")
    #     return StudentCourse.objects.filter(lecture_table=lecture[0])

class StudentCourseDetail(LoginRequiredMixin, DetailView):
    model = StudentCourse
    template_name = 'teacher/studentcourse_detail.html'

    def get_queryset(self):
        return StudentCourse.objects.raw("SELECT student_table_id FROM student_studentcourse where lecture_table_id=10000;")