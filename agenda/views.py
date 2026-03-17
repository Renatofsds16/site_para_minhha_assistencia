from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Agenda
from .form import AgendaForm

@login_required
def lista_agenda(request):
    agendamentos = Agenda.objects.filter(empresa=request.user.perfil.empresa).order_by('data', 'hora')
    return render(request, 'agenda/lista.html', {
        'agendamentos': agendamentos
    })



@login_required
def nova_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.empresa  = request.user.perfil.empresa
            agenda.save()
            return redirect('agenda:lista')
    else:
        form = AgendaForm()

    return render(request, 'agenda/form.html', {'form': form})


@login_required
def editar_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id,empresa=request.user.perfil.empresa)

    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            return redirect('agenda:lista')
    else:
        form = AgendaForm(instance=agenda)

    return render(request, 'agenda/form.html', {'form': form})


@login_required
def remover_agenda(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id,empresa=request.user.perfil.empresa)
    agenda.delete()
    return redirect('agenda:lista')
