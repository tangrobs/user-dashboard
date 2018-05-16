from django.shortcuts import render, redirect, HttpResponse
from .models import *
from apps.login.models import User, UserManager
from django.contrib import messages


def dashboard(request):
    context = { "user": User.objects.all()}
    return render(request, "dashboard/dashboard.html", context)