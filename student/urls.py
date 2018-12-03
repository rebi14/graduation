from django.urls import path
from student import views
from django.conf.urls import include


urlpatterns = [
    path('', views.index, name='index')
]



# urlpatterns = [
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
#     path('accounts/signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
#     path('accounts/signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
# ]


urlpatterns += [
    path('all-lectures', views.GetAllCourse.as_view(), name='all-lectures'),
    path('student-lecture', views.GetStudentLecture.as_view(), name='student-lecture'),
    path('enrolment', views.enrolment, name='lecture-enrolment'),
    path('create-lecture', views.CreateLecture.as_view(), name='create-lecture'),
    path('teacher-lectures', views.GetTeacherLecture.as_view(), name='teacher-lecture'),
    path('lecture-detail/<int:pk>', views.GetLectureStudentList.as_view(), name='lecture-detail'),
    path('upload-photo', views.upload_image, name='upload-photo'),
]