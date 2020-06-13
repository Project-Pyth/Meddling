from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

from  accounts import views


app_name='accounts'
urlpatterns = [
    path('', views.home, name='index'),
    path('feedback/',views.feedback, name='feedback'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('category/<pk>', views.sub_pdf, name='sub_pdf'),
    path('aboutus', views.aboutus, name='aboutus'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('quiz',views.quiz, name='quiz'),
    path('pdf/<pk>',views.pdf, name='pdf'),
    path('profile/',views.profile, name="profile"),
    path('editprofile/',views.editprofile, name="editprofile"),
    url('changepass',views.changepass,name="changepass")
    # url(r'^(?P<choices>[\w]+)' , views.questions, name = 'questions'),
    # url('cate/', views.category, name='category'),


]
