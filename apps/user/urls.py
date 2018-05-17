from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^show/(?P<id>\d+)/$', views.show),
    #url(r'^edit$', views.edit),
    url(r'^edit/(?P<id>\d+)/$', views.edit),
    url(r'^new/$', views.new),
    url(r'^processnew/$', views.processnew),
    url(r'^processedit/(?P<id>\d+)/$', views.processedit),
    url(r'^processedit/(?P<id>\d+)/(?P<switch>\w)/$', views.switchhandler),
    url(r'^addmessage/$', views.addmessage),
    url(r'^addcomment/$', views.addcomment),
    url(r'^deleteuser/(?P<id>\d+)/$', views.deleteuser),

]