from django.shortcuts import render, redirect, HttpResponse
from .models import *
from apps.login.models import User, UserManager
from django.contrib import messages

def show(request, id):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login')
    else:
        user = User.objects.get(id = id)
        context = {
            'user': user
        }
        return render(request, "user/showuser.html",context)

def edit(request, id):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login')
    elif User.objects.get(id = request.session['userid']).admin:
        context = {
            'user':User.objects.get(id = id)
        }
        return render(request, "user/edituser.html", context)
    elif request.session['userid'] == id:
        context = {
            'user':User.objects.get(id = request.session['userid'])
        }
        return render(request, "user/edituser.html", context)
    else:
        messages.error(request, "You do not have acces to this page")
        return redirect('/dashboard')
    
""" def adminedit(request, id):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/signin')
    elif User.objects.get(id = request.session['userid']).admin:
        context = {
            'user':User.objects.get(id = id)
        }
        return render(request, "user/edituser.html", context)
    else:
        messages.error(request, "You cannot acces this page if you are not an admin")
        return redirect('/dashboard')
 """
def new(request):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login')
    elif User.objects.get(id = request.session['userid']).admin:
        return render(request, "user/newuser.html")
    else:
        messages.error(request, "You cannot acces this page if you are not an admin")
        return redirect('/dashboard')

def processnew(request):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login')
    elif not User.objects.get(id = request.session['userid']).admin:
        return redirect('/dashboard')
    elif request.method == 'POST':
        validation_return = User.objects.registration_validator(request.POST)
        if "error_messages" in validation_return:
            for value in validation_return["error_messages"].values():
                messages.error(request, value)
            return redirect('/users/new')
        elif "user" in validation_return:
            messages.success(request,"Succesfully created user!")
            return redirect('/dashboard/admin')
        else:
            print("something went wrong")
            return redirect('/')
    else:
        return redirect('/dashboard/admin')

def processedit(request,id):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login')
    elif User.objects.get(id = request.session['userid']).admin:
        if request.method == 'POST':
            validation_return = User.objects.registration_validator(request.POST)
            if "error_messages" in validation_return:
                for value in validation_return["error_messages"].values():
                    messages.error(request, value)
                return redirect('/users/edit/{}'.format(id))
            elif "user" in validation_return:
                messages.success(request,"Succesfully edited!")
                return redirect('/dashboard/admin')
            else:
                print("something went wrong")
                return redirect('/')
        else:
            return redirect('/dashboard/admin')
    elif not User.objects.get(id = request.session['userid']).admin:
        if request.method == 'POST':
            validation_return = User.objects.registration_validator(request.POST)
            if "error_messages" in validation_return:
                for value in validation_return["error_messages"].values():
                    messages.error(request, value)
                return redirect('/users/edit/{}'.format(id))
            elif "user" in validation_return:
                messages.success(request,"Succesfully edited!")
                return redirect('/dashboard')
            else:
                print("something went wrong")
                return redirect('/')
        else:
            return redirect('/dashboard')
 

def checkloggedin(request):
    if 'userid' not in request.session:
        return False
    return True
