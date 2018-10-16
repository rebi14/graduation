from django.urls import path
from student import views
from django.conf.urls import include


urlpatterns = [
    path('', views.index, name='index')
]

urlpatterns += [
    path('photo/', views.upload_image, name='upload-photo'),
]

