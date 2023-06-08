from django.conf.urls import url

from . import views

app_name='RGS'
urlpatterns=[
    # Main functionalities
    url(r'^home/$', views.HomeView.dashboard, name='home'),
    url(r'^manual/$', views.HomeView.manual_control, name='manual'),
    url(r'^auto/$', views.HomeView.auto_flight, name='auto'),
]