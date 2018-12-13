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
    path('all-lectures2', views.GetAllCourse2.as_view(), name='all-lectures2'),
    path('student-lecture', views.GetStudentLecture.as_view(), name='student-lecture'),
    path('enrolment', views.enrolment, name='lecture-enrolment'),
    path('create-lecture', views.CreateLecture.as_view(), name='create-lecture'),
    path('teacher-lectures', views.GetTeacherLecture.as_view(), name='teacher-lecture'),
    path('lecture-detail/crn=<int:pk>', views.GetLectureStudentList.as_view(), name='lecture-detail'),
    path('upload-photo', views.student_photo_upload, name='upload-photo'),
    path('class-photo-upload', views.class_photo_upload, name='class-photo-upload'),
    path('attendance-list', views.AttendanceListView.as_view(), name='attendance-list'),
    path('take-attendance', views.AttendanceView.as_view(), name='take-attendance')
]
