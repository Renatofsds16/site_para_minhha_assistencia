from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .forms import CadastroForm
from .models import Perfil, Empresa


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
            )

            login(request, user)
            return redirect('dashboard')
    else:
        form = CadastroForm()

    return render(request, 'accounts/cadastro.html', {
        'form': form
    })



def login_view(request):

    if request.user.is_authenticated:
        return redirect('/')

    erro = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            erro = "Usuário ou senha inválidos"

    return render(request, 'auth/login.html', {
        'erro': erro
    })
