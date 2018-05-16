from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$',views.index),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
]