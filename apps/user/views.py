from django.shortcuts import render, redirect, HttpResponse
from .models import *
from apps.login.models import User, UserManager
from apps.dashboard.models import *
from django.contrib import messages
import bcrypt
def show(request, id):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login')
    else:
        user = User.objects.get(id = id)
        context = {
            'user': user,
            'message': user.received_messages.all().order_by("-created_at")
        }
        return render(request, "user/showuser.html",context)

def edit(request, id):
    print("entering edit")
    print(checkloggedin(request))
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

def processedit(request, id):
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

def switchhandler(request, id, switch):
    info = {}
    me = User.objects.get(id = id)
    if switch == 'a':
        info['first_name'] = request.POST['first_name']
        info['last_name'] = request.POST['last_name']
        info['email'] = request.POST['email']
        returnvalid = User.objects.edit_validator(info, id)
        if returnvalid['status']:
            return redirect('/users/show/{}'.format(id))
        else:
            for value in returnvalid['error_messages'].values():
                messages.error(request, value)
            return redirect('/users/edit/{}'.format(id))
    if switch == 'b':
        if len(request.POST['password']) < 8:
            messages.error(request,"Password must be at least 8 characters")
            return redirect('/users/edit/{}'.format(id))
        elif request.POST['password'] != request.POST['passconfirm']:
            messages.error(request,"Passwords do not match")
            return redirect('/users/edit/{}'.format(id))
        else:
            phash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            me.pwhash = phash
            me.save()
            return redirect('/users/show/{}'.format(id))
    if switch == 'c':
        print("entering switch statemente c")
        print(request.POST['description'])
        me.description.content = request.POST['description']
        me.description.save()
        print(me.description.content)
        return redirect('/users/show/{}'.format(id))

def addmessage(request):
    print(request.method)
    if request.method == "POST":
        id = request.POST['id']
        content = request.POST['content']
        Message.objects.create(content = content, receiver = User.objects.get(id = id), \
                            sender = User.objects.get(id = request.session['userid']))
        return redirect('/users/show/{}/'.format(id))
    else:
        return HttpResponse("flagrant error")

def addcomment(request):
    print(request.method)
    if request.method == "POST":
        id = request.POST['id']
        content = request.POST['content']
        Comment.objects.create(content = content, message = Message.objects.get(id = request.POST['id']), \
                                    sender = User.objects.get(id = request.session['userid']))
        return redirect('/users/show/{}/'.format(request.POST['target_id']))
    else:
        return HttpResponse("flagrant error")

def deleteuser(request, id):
    if not checkloggedin(request):
        messages.error(request,"Please login to access this page")
        return redirect('/login/')
    elif not User.objects.get(id = request.session['userid']).admin:
        messages.error(request, "You cannot delete users")
        return redirect('/dashboard/')
    else:
        User.objects.get(id = id).delete()
        return redirect('/dashboard/')



 

def checkloggedin(request):
    if 'userid' not in request.session:
        return False
    return True
