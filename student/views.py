import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, render_to_response
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView, View
from student.forms import StudentSignUpForm, TeacherSignUpForm, EnrollLectureForm, CreateLectureForm, StudentPhotoForm, \
    ClassPhotoForm
from student.models import *
from django.views import generic
from django.contrib import messages


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

            try:
                Lecture.objects.get(lecture_crn=a.lecture_table.lecture_crn)
            except (ObjectDoesNotExist, AttributeError):
                raise Http404("aaa")

            lec = Lecture.objects.get(lecture_crn=a.lecture_table.lecture_crn)
            stu = Student.objects.get(student_no=request.user.username)

            enrolled_course = StudentCourse.objects.filter(student_table=stu)
            enrolled_course_id_list = list()
            for i in enrolled_course:
                enrolled_course_id_list.append(str(i.lecture_table.course_id))

            if str(lec.course_id) in enrolled_course_id_list:
                messages.add_message(request, messages.INFO, f'{lec.course_id} kodlu derse kaydınız vardır.')
                return render(request, 'student/enrolment.html', {'form': form, 'some_flag': True})
            else:
                StudentCourse.objects.create(lecture_table=lec, student_table=stu)
                return redirect('student-lecture')
    else:
        form = EnrollLectureForm()

    return render(request, 'student/enrolment.html', {'form': form})


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def index(request):

    return render(request, 'index.html')


class GetAllCourse(LoginRequiredMixin, generic.ListView):

    model = Lecture
    template_name = "student/all_lecture.html"

    def get_queryset(self):
        return Lecture.objects.all()


class GetAllCourse2(LoginRequiredMixin, generic.ListView):

    model = Lecture
    template_name = "teacher/all_lecture2.html"

    def get_queryset(self):
        return Lecture.objects.all()


class GetStudentLecture(LoginRequiredMixin, generic.ListView):

    model = Lecture
    template_name = "student/student_course.html"
    # context_object_name = 'student_lecture_list'

    def get_queryset(self):
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


class GetTeacherLecture(LoginRequiredMixin, ListView):
    model = Lecture
    template_name = 'teacher/teacher_lecture.html'

    def get_queryset(self):
        teacher = Teacher.objects.get(teacher_no=self.request.user.username)
        return Lecture.objects.filter(teacher_no=teacher)

    # def get(self, request, *args, **kwargs):
    #     lec = Lecture.objects.get(lecture_crn=self.request.session['crn'])
    #     enrolled = len(StudentCourse.objects.filter(lecture_table=lec))
    #     context = locals()
    #     context['enrolled'] = enrolled
    #     return render_to_response(self.template_name, context)




class GetLectureStudentList(LoginRequiredMixin, ListView):
    model = StudentCourse
    template_name = 'teacher/lecture_detail.html'

    def get_queryset(self):
        a = self.request.path
        crn = re.findall(r'[0-9].*', a)
        lec = Lecture.objects.get(lecture_crn=crn[0])
        self.request.session['crn'] = crn[0]
        return StudentCourse.objects.filter(lecture_table=lec)


def student_photo_upload(request):
    if request.method == 'POST':
        form = StudentPhotoForm(request.POST, request.FILES)
        print(request.FILES['document'].name)
        request.FILES['document'].name = str(request.user.username) + ".jpg"
        if form.is_valid():
            form.save()
            return render(request, 'student/student_photo_upload.html', {'form': form})
    else:
        form = StudentPhotoForm()
    return render(request, 'student/student_photo_upload.html', {'form': form})


def class_photo_upload(request):
    if request.method == 'POST':
        form = ClassPhotoForm(request.POST, request.FILES)
        request.FILES['document'].name = str(request.session['crn']) + ".jpg"
        if form.is_valid():
            form.save()
            return render(request, 'teacher/class_photo_upload.html', {'form': form})

    else:
        form = ClassPhotoForm()
    return render(request, 'teacher/class_photo_upload.html', {'form': form})


class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'teacher/attendance_list.html'

    def get_queryset(self):
        lecture = Lecture.objects.get(lecture_crn=self.request.session['crn'])
        return Attendance.objects.filter(lecture_crn=lecture)


class AttendanceView(LoginRequiredMixin, View):
    model = Attendance
    template_name = "teacher/attendance_update.html"

    def take_att(self):
        crn = self.request.session['crn']
        lecture = Lecture.objects.get(lecture_crn=crn)
        student_courses = StudentCourse.objects.filter(lecture_table=lecture)
        sinif_listesi = list()
        for i in student_courses:
            sinif_listesi.append(str(i.student_table.student_no))
        olanlar = ['090120510', '050120478', 'student1']

        for i in sinif_listesi:
            if i in olanlar:
                lec = Lecture.objects.get(lecture_crn=self.request.session['crn'])
                stu = Student.objects.get(student_no=i)
                Attendance.objects.create(student_id=stu, lecture_crn=lec,
                                          date_attended=datetime.datetime.now(), inout=True)
            else:
                stu = Student.objects.get(student_no=i)
                lec = Lecture.objects.get(lecture_crn=self.request.session['crn'])
                Attendance.objects.create(student_id=stu, lecture_crn=lec,
                                          date_attended=datetime.datetime.now(), inout=False)

    def get(self, request):
        self.take_att()
        return render(request, 'teacher/attendance_update.html')
