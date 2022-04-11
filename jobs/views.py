from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Jobs
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User

# Create your views here.
def find_jobs(request):
    if request.method == 'GET':
        preco_minimo = request.GET.get('preco_minimo')
        preco_maximo = request.GET.get('preco_maximo')

        prazo_minimo = request.GET.get('prazo_minimo')
        prazo_maximo = request.GET.get('prazo_maximo')

        categoria = request.GET.get('categoria')

        if preco_minimo or preco_maximo or prazo_minimo or prazo_maximo or categoria:
            if not preco_minimo:
                preco_minimo = 0

            if not preco_maximo:
                preco_maximo = 999999

            if not prazo_minimo:
                prazo_minimo = datetime(year=1900, month=1, day=1)

            if not prazo_maximo:
                prazo_maximo = datetime(year=3000, month=1, day=1)
            

            if categoria == 'D':
                categoria = ['D',]
            elif categoria == 'EV':
                categoria = ['EV',]

            jobs = Jobs.objects.filter(preco__gte=preco_minimo)\
                .filter(preco__lte=preco_maximo)\
                .filter(prazo_entrega__gte=prazo_minimo)\
                .filter(prazo_entrega__lte=prazo_maximo)\
                .filter(categoria__in=categoria)\
                .filter(reservado=False)
        else:
            jobs = Jobs.objects.filter(reservado=False)

        return render(request, 'find_jobs.html', {'jobs': jobs})


def aceitar_job(request, id):
    job = Jobs.objects.get(id=id)
    job.profissional = request.user
    job.reservado = True
    job.save()
    return redirect('/jobs/find_jobs')


def perfil(request):
    if request.method == "GET":
       jobs = Jobs.objects.filter(profissional=request.user)
       return render(request, 'perfil.html', {'jobs': jobs})
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')

        usuario = User.objects.filter(username=username).exclude(id=request.user.id)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse Username')
            return redirect('/jobs/perfil')

        usuario = User.objects.filter(email=email).exclude(id=request.user.id)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse E-mail')
            return redirect('/jobs/perfil')

        
        request.user.username = username
        request.user.email = email
        request.user.first_name = primeiro_nome
        request.user.last_name = ultimo_nome
        request.user.save()

        messages.add_message(request, constants.SUCCESS, 'Dados alterado com sucesso')
        return redirect('/jobs/perfil')