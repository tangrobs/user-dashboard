from django.conf.urls import url, include #pylint: disable = E0401

urlpatterns = [
    url(r'^users', include('apps.user.urls')),
    url(r'^dashboard', include('apps.dashboard.urls')),
    url(r'^', include('apps.login.urls'))
]