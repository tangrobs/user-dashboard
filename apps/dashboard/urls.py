from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^/$', views.dashboard),
    url(r'^admin/$', views.dashboard)
]