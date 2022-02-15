from time import timezone
from django.db import IntegrityError
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .forms import todoform
from .models import list
from django.utils import timezone
from todo.forms import todoform
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'todo/home.html')

def signupme(request):
    if request.method=='GET':
        return render(request,'todo/signup.html',{'form': UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try: 
                user= User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodo')

            except IntegrityError:
                return render(request,'todo/signup.html',{'form': UserCreationForm(),'error':'Username already taken'})
        else:
            return render(request,'todo/signup.html',{'form': UserCreationForm(),'error':'Password do not match'}) 

@login_required
def logoutme(request)  :
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginme(request):
    if request.method=='GET':
        return render(request,'todo/login.html',{'form': AuthenticationForm()})
    else:
        user= authenticate(request, username = request.POST['username'],password= request.POST['password'])
        if user is None:
            return render(request,'todo/login.html',{'form': AuthenticationForm(),'error':'Username and password did not match'})

        else:
            login(request,user)
            return redirect('currenttodo')
               
@login_required
def currenttodo(request) :
    todos = list.objects.filter(user=request.user, completed__isnull=True).order_by('-completed')
    return render(request,'todo/todos.html',{'todos':todos})

@login_required
def previoustodo(request) :
    todos = list.objects.filter(user=request.user, completed__isnull=False)
    return render(request,'todo/previoustodos.html',{'todos':todos})

@login_required
def viewtodo(request,todo_pk) :
    if request.method=='GET':
        todo= get_object_or_404(list, pk= todo_pk,user= request.user)
        form = todoform(instance=todo)
        return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':"Invalid data entry"})
    else:
        try:
            todo= get_object_or_404(list, pk= todo_pk, user= request.user)
            form = todoform(request.POST,instance=todo)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo':todo,'form':form,'error':"Invalid data entry"})


@login_required    
def createtodo(request):
    if request.method=='GET':
        return render(request,'todo/createtodo.html',{'form': todoform()})
    else:
        try:
            form = todoform(request.POST)
            newtodo= form.save(commit=False)
            newtodo.user= request.user
            newtodo.save()
            return redirect('currenttodo')
        except:
            return render(request,'todo/createtodo.html',{'form': todoform(),'error':"Invalid Data entry"})

@login_required
def completetodo(request,todo_pk):
    todo= get_object_or_404(list, pk= todo_pk, user= request.user)
    if request.method=='POST':
        todo.completed= timezone.now()
        todo.save()
        return redirect('currenttodo')

def deletetodo(request,todo_pk):
    todo= get_object_or_404(list, pk= todo_pk, user= request.user)
    if request.method=='POST':
        todo.delete()
        return redirect('currenttodo')



