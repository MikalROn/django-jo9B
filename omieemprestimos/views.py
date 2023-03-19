import os
import asyncio
import datetime as dt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormLoja, LancarEmprestimo
from .models import Emprestimos, Lojas
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from pyrogram import Client
from dotenv import load_dotenv


load_dotenv()

CHAT_ID = '-979899802'
BOT_ATIVADO = True
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def telegram_bot(msg: str):
    if BOT_ATIVADO:
        async def enviar_mensagem():
            async with Client('BotDeEMprestimos', api_hash=API_HASH, api_id=API_ID, bot_token=BOT_TOKEN) as client:
                    await client.send_message(CHAT_ID, msg)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(enviar_mensagem())
        loop.close()

@login_required
def index(request):
    return render(request, 'index.html', {
        'lojas':Lojas.objects.all(),
        'emprestimos':Emprestimos.objects.all(),
        'form_loja':FormLoja,
        'form_emprestimo':LancarEmprestimo
    })

@login_required
def lojas(request, id_loja):
    loja = Lojas.objects.get(pk=id_loja)
    emprestou = Emprestimos.objects.filter(credor__nome=loja.nome)
    deve = Emprestimos.objects.filter(devedor__nome=loja.nome)
    
    return render(request, 'loja.html', {
        'loja':loja,
        'emprestou':emprestou,
        'deve':deve
    })

@login_required
def emprestimo(request, id_emprestimo):
    emprestimo = Emprestimos.objects.get(pk=id_emprestimo)
    return render(request, 'emprestimo.html', {
        'emprestimo':emprestimo
    })

@login_required
def cadastra_loja(request):
    if request.method == 'POST':
        form = FormLoja(request.POST)
        if form.is_valid():
            data = Lojas(nome=form.cleaned_data['nome'])
            data.save()
        return HttpResponseRedirect(reverse('index'))

@login_required
def lancar_emprestimo(request):
    if request.method == 'POST':
        form = LancarEmprestimo(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            credor =  Lojas.objects.get(nome=data['credor'])
            devedor = Lojas.objects.get(nome=data['devedor'])

            db = Emprestimos(
                credor=credor,
                devedor=devedor,
                data=data['data'],
                valor=data['valor'],
                status='DEVENDO'
            )
            db.save()
            telegram_bot(f'{db}')
        return HttpResponseRedirect(reverse('index'))

@login_required       
def editar_emprestimo(request, id_emprestimo):
    if request.method == 'GET':
        emprestimo = Emprestimos.objects.get(pk=id_emprestimo)
        form = LancarEmprestimo({
            'data':emprestimo.data,
            'credor':emprestimo.credor,
            'devedor':emprestimo.devedor,
            'valor':emprestimo.valor
            
        })
        return render(request, 'editar_emprestimo.html', {
            'form_loja':form,
            'emprestimo':emprestimo
            })
    elif request.method == 'POST':
        objeto = Emprestimos.objects.get(pk=id_emprestimo)
        form = LancarEmprestimo(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            credor =  Lojas.objects.get(nome=data['credor'])
            devedor = Lojas.objects.get(nome=data['devedor'])
            db = Emprestimos(
                pk=id_emprestimo,
                credor=credor,
                devedor=devedor,
                data=data['data'],
                valor=data['valor'],
                status='DEVENDO'
            )
            db.save()
            msg = f'''
            Emprestimo Editado de {objeto}:
            Para -> {db}
            '''
            telegram_bot(msg)
            return HttpResponseRedirect(reverse('index'))

    else:
        HttpResponseNotAllowed(reverse('index'))
  
@login_required  
def pagar_emprestimo(request, id_emprestimo):
    objeto = Emprestimos.objects.get(pk=id_emprestimo)
    objeto.status = 'PAGO'
    objeto.save()
    telegram_bot(f'Emprestimo {objeto} foi pago!💵💵💵')
    return HttpResponseRedirect(reverse('index'))

@login_required
def cancela_emprestimo(request, id_emprestimo):
    objeto = Emprestimos.objects.get(pk=id_emprestimo)
    objeto.delete()
    telegram_bot(f'Emprestimo {objeto} Cancelado !')
    return HttpResponseRedirect(reverse('index'))

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
