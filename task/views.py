from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from task.forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'GET':
        return render(request, 'singup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:

                user =  User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])

                user.save()
                login(request, user)
                return redirect('task')
            
            except IntegrityError:
                return render(request, 'singup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe en memoria'
                })
        return render(request, 'singup.html', {
            'form': UserCreationForm,
            'error': 'Las password son distintas entre si'
        })


def singin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o clave es incorrecto'
            })
        else:
            login(request, user)
            return redirect('task')

        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })



def home(request):
    return render(request, 'home.html')

def vueltaInicio(request):
    return redirect('home')


@login_required
def task_detail(request, task_id):
    print('Task')
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form,
                                                        'error': "Error actualizando"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('task')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')

@login_required
def task(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull= True)
    return render(request, 'task.html', {'tasks': tasks})


@login_required
def task_completed(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull= False).order_by('-datecompleted')
    return render(request, 'task.html', {'tasks': tasks})

def cerrar_sesion(request):
    logout(request)
    return redirect('home')


@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            formularioNuevo = TaskForm(request.POST).save(commit=False)
            formularioNuevo.user = request.user
            formularioNuevo.save()
            return redirect('task')
        except:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor, rellene de forma correcta los campos'
            })