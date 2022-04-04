from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

# Create your views here.

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/plataforma')
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('/auth/register')

        if len(username.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'O username e a senha não podem estar vazios')
            return redirect('/auth/register')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuario já existe')
            return redirect('/auth/register')

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            return redirect('/auth/login')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno')
            return redirect('/auth/register')
        

def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/plataforma')
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if not user:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            return redirect('/plataforma')


def sair(request):
    auth.logout(request)
    return redirect('/auth/login')