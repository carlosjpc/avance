# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from admon.models import Cuenta_Bancaria
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
            url = reverse('detalle_agencia', kwargs={'pk': agencia.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'admon/nueva_cb.html',
                          {'cuenta_bancariaform': cuenta_bancariaform,
                           'agencia': agencia, })
    else:
        cuenta_bancariaform = Cuenta_BancariaForm()
    return render(request, 'admon/nueva_cb.html', {'form': cuenta_bancariaform,
                                                   'agencia': agencia, })


@login_required
def editar_cuentab_agencia(request, pk):
    user = request.user
    cuenta_agencia = Cuenta_Bancaria.objects.get(pk=pk)
    if user.groups.filter(name='comercial_vendedor').exists():
        if not user == cuenta_agencia.Agencia.Atiende:
            return Http404
    if request.method == "POST":
        cuentaform = Cuenta_BancariaForm(request.POST, instance=cuenta_agencia)
        if cuentaform.is_valid():
            cuenta = cuentaform.save()
            url = reverse('detalle_agencia',
                          kwargs={'pk': cuenta_agencia.Agencia.pk})
            return HttpResponseRedirect(url)
    cuentaform = Cuenta_BancariaForm(instance=cuenta_agencia)
    return render(request, 'comercial/form.html', {'form': cuentaform, })


class Cuenta_BDelete(DeleteView):
    model = Cuenta_Bancaria
    template_name = 'comercial/confirm_delete.html'
    success_url = reverse_lazy('redirect')

    def get_object(self, queryset=None):
        """ Hook to ensure object owner is request.user """
        cuenta = super(Cuenta_BDelete, self).get_object()
        if self.request.user.groups.filter(name='comercial_vendedor').exists():
            if not cuenta.Agencia.Atiende == self.request.user:
                raise Http404
        return cuenta
