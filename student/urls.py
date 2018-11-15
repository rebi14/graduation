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
    path('all-lectures',views.GetAllCourse.as_view(), name='all-lectures'),
]