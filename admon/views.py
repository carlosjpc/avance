from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test

from admon.forms import Cuenta_BancariaForm

from comercial.models import Agencia_Automotriz

@login_required
def nueva_cuenta_bancaria_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        agencia = Agencia_Automotriz.objects.get(Atiende=user, pk=pk)
    else:
        agencia = Agencia_Automotriz.objects.get(pk=pk)
    if request.method == 'POST':
        cuenta_bancariaform = Cuenta_BancariaForm(request.POST)
        if cuenta_bancariaform.is_valid():
            nueva_cb_agencia = cuenta_bancariaform.save(commit=False)
            nueva_cb_agencia.Agencia = agencia
            nueva_cb_agencia.save()
        else:
            return render(request, 'admon/nueva_cb.html', {'cuenta_bancariaform': cuenta_bancariaform, 'agencia': agencia,})
    else:
        cuenta_bancariaform = Cuenta_BancariaForm()
    return render(request, 'admon/nueva_cb.html', {'form': cuenta_bancariaform, 'agencia': agencia,})
