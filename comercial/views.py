# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from itertools import chain
from django.utils.safestring import mark_safe

# reportlab imports
from io import BytesIO
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak,
                                TableStyle, Spacer)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# app imports
from comercial.utils import next_weekday, comparativaPDF
from comercial.utils import AgendaCalendar

from comercial.models import (Cliente, Contacto_C, Direccion_Fiscal_Cliente,
                              Agencia_Automotriz, Contacto_Agencia, Caso,
                              Interaccion, Anotacion, Historial_Etapa, Cita,
                              Equipo_Solicitado)

from comercial.forms import (ClienteForm, Cliente_VForm, Contacto_CForm,
                             Contacto_CCForm, Contacto_CCAForm,
                             Caso_VForm, Caso_CVForm, Caso_IniForm,
                             Caso_StatusForm, Equipo_SolicitadoForm,
                             Agencia_AutomotrizForm, Agencia_AutomotrizVForm,
                             Contacto_Agencia_IniForm,
                             Direccion_Fiscal_ClienteForm,
                             Direccion_Fiscal_ClienteCForm, InteraccionForm,
                             AnotacionForm, CitaClienteForm, CitaAgenciaForm,
                             OC_Form, ComparativaForm)

from central.models import (Documentacion_PMoral, Documentacion_PFisica,
                            Contrato, Anexo, Factura)

from central.forms import (Documentacion_PMoral_Form,
                           Documentacion_PFisica_Form)

from admon.models import Cuenta_Bancaria

# functions for decoraters to determine if a user can create / edit / delete:


def comercial_check(user):
    if user:
        return user.groups.filter(name='Comercial').count() == 1
    return False


def backup_check(user):
    if user.groups.filter(name='comercial_backup').exists(
                         ) or user.groups.filter(
                         name='comercial_mger').exists():
        return True
    return False


def manager_check(user):
    if user:
        return user.groups.filter(name='comercial_mger').count() == 1
    return False


def vendedor_check(user):
    if user.groups.filter(name='comercial_vendedor').exists(
                         ) or user.groups.filter(
                         name='comercial_mger').exists():
        return True
    return False

# Create your views here.

# -------------------------------- Views Ctrl Panels --------------------------


@login_required
@user_passes_test(vendedor_check)
def ctrl_panel_vendedor(request):
    user = request.user
    today = datetime.today()
    slash_date = datetime.today() - timedelta(days=3)
    try:
        rechazados = Historial_Etapa.objects.filter(
                                        Etapa='rzo', Caso__Atiende=user,
                                        Fecha__range=(slash_date, today))
    except ObjectDoesNotExist:
        pass
    lista_casos_int = Caso.objects.filter(Atiende=user, Etapa='int')
    lista_anotacion_int = []
    for caso in lista_casos_int:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_int.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_cot = Caso.objects.filter(Atiende=user, Etapa='cot')
    lista_anotacion_cot = []
    for caso in lista_casos_cot:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_cot.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_epa = Caso.objects.filter(Atiende=user, Etapa='epa')
    lista_anotacion_epa = []
    for caso in lista_casos_epa:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_epa.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_eap = Caso.objects.filter(Atiende=user, Etapa='eap')
    lista_anotacion_eap = []
    for caso in lista_casos_eap:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_eap.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_apr = Caso.objects.filter(Atiende=user, Etapa='apr')
    lista_anotacion_apr = []
    for caso in lista_casos_apr:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_apr.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_cfr = Caso.objects.filter(Atiende=user, Etapa='cfr')
    lista_anotacion_cfr = []
    for caso in lista_casos_cfr:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_cfr.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_pir = Caso.objects.filter(Atiende=user, Etapa='pir')
    lista_anotacion_pir = []
    for caso in lista_casos_pir:
        try:
            ultima_anotacion = Anotacion.objects.filter(
                                            al_Caso=caso).latest('Fecha')
            lista_anotacion_pir.append(ultima_anotacion)
        except ObjectDoesNotExist:
            pass
    lista_casos_fon = Caso.objects.filter(Atiende=user, Etapa='fon')
    mes = datetime.today()
    hist_cerrados_em = Historial_Etapa.objects.filter(
                            Etapa='crd', Fecha__month=mes.month)
    context = {'lista_casos_int': lista_casos_int,
               'lista_anotacion_int': lista_anotacion_int,
               'lista_casos_cot': lista_casos_cot,
               'lista_anotacion_cot': lista_anotacion_cot,
               'lista_casos_epa': lista_casos_epa,
               'lista_anotacion_epa': lista_anotacion_epa,
               'lista_casos_eap': lista_casos_eap,
               'lista_anotacion_eap': lista_anotacion_eap,
               'lista_casos_apr': lista_casos_apr,
               'lista_anotacion_apr': lista_anotacion_apr,
               'lista_casos_cfr': lista_casos_cfr,
               'lista_anotacion_cfr': lista_anotacion_pir,
               'lista_casos_pir': lista_casos_pir,
               'lista_anotacion_pir': lista_anotacion_pir,
               'lista_casos_fon': lista_casos_fon,
               'lista_casos_crd': hist_cerrados_em,
               'rechazados': rechazados, }
    return render(request, 'comercial/ctrl_panel_vendedor.html', context)


@login_required
@user_passes_test(backup_check)
def ctrl_panel_backup(request):
    casos_int = Caso.objects.filter(Etapa='int')
    documentacion_int = []
    for caso in casos_int:
        if caso.Cliente.Persona_Moral is True:
            try:
                documentacion = Documentacion_PMoral.objects.get(Caso=caso)
                documentacion_int.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_int.append(None)
        elif caso.Cliente.Persona_Moral is False:
            try:
                documentacion = Documentacion_PFisica.objects.get(Caso=caso)
                documentacion_int.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_int.append(None)
    listas_int = zip(casos_int, documentacion_int)
    casos_cot = Caso.objects.filter(Etapa='cot')
    documentacion_cot = []
    for caso in casos_cot:
        if caso.Cliente.Persona_Moral is True:
            try:
                documentacion = Documentacion_PMoral.objects.get(Caso=caso)
                documentacion_cot.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_cot.append(None)
        elif caso.Cliente.Persona_Moral is False:
            try:
                documentacion = Documentacion_PFisica.objects.get(Caso=caso)
                documentacion_cot.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_cot.append(None)
    listas_cot = zip(casos_cot, documentacion_cot)
    casos_epa = Caso.objects.filter(Etapa='epa')
    documentacion_epa = []
    for caso in casos_epa:
        if caso.Cliente.Persona_Moral is True:
            try:
                documentacion = Documentacion_PMoral.objects.get(Caso=caso)
                documentacion_epa.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_epa.append(None)
        elif caso.Cliente.Persona_Moral is False:
            try:
                documentacion = Documentacion_PFisica.objects.get(Caso=caso)
                documentacion_epa.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_epa.append(None)
    listas_epa = zip(casos_epa, documentacion_epa)
    casos_eap = Caso.objects.filter(Etapa='eap')
    documentacion_eap = []
    for caso in casos_eap:
        if caso.Cliente.Persona_Moral is True:
            try:
                documentacion = Documentacion_PMoral.objects.get(Caso=caso)
                documentacion_eap.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_eap.append(None)
        elif caso.Cliente.Persona_Moral is False:
            try:
                documentacion = Documentacion_PFisica.objects.get(Caso=caso)
                documentacion_eap.append(documentacion)
            except ObjectDoesNotExist:
                documentacion_eap.append(None)
    listas_eap = zip(casos_eap, documentacion_eap)
    casos_apr = Caso.objects.filter(Etapa='apr')
    casos_cfr = Caso.objects.filter(Etapa='cfr')
    casos_pir = Caso.objects.filter(Etapa='pir')
    casos_fon = Caso.objects.filter(Etapa='fon')
    casos_crd = Caso.objects.filter(Etapa='crd').order_by('-id')[:3]
    context = {'listas_int': listas_int,
               'listas_cot': listas_cot,
               'listas_epa': listas_epa,
               'listas_eap': listas_eap,
               'lista_casos_apr': casos_apr,
               'lista_casos_cfr': casos_cfr,
               'lista_casos_pir': casos_pir,
               'lista_casos_fon': casos_fon,
               'lista_casos_crd': casos_crd, }
    return render(request, 'comercial/ctrl_panel_backup.html', context)

# ---------------------------- Views Citas -----------------------------


@login_required
@user_passes_test(vendedor_check)
def nueva_cita_cliente(request):
    if request.method == 'POST':
        citaform = CitaClienteForm(request.POST, user=request.user)
        if citaform.is_valid():
            nueva_cita = citaform.save(commit=False)
            nueva_cita.Atiende = request.user
            nueva_cita.save()
            url = reverse('redirect')
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/form_wdate.html', {
                                                        'form': citaform})
    citaform = CitaClienteForm(instance=Cita(), user=request.user)
    return render(request, 'comercial/form_wdate.html', {
                                'form': citaform, 'title': "Nueva Cita:", })


@login_required
@user_passes_test(vendedor_check)
def nueva_cita_agencia(request):
    if request.method == 'POST':
        citaform = CitaAgenciaForm(request.POST, user=request.user)
        if citaform.is_valid():
            agencia = citaform.cleaned_data.get('Agencia')
            dias = citaform.cleaned_data.get('Todos_los')
            hora = citaform.cleaned_data.get('Hora')
            today = datetime.now()
            if "6" in dias:
                for dia in dias:
                    if not dia == "6":
                        fecha = next_weekday(today, dia)
                        nueva_cita = Cita(Agencia=agencia,
                                          Atiende=request.user,
                                          Hora=hora, Fecha=fecha,
                                          Descripcion=agencia.get_Marca_display())
                        nueva_cita.save()
            else:
                for dia in dias:
                    next_dia = next_weekday(today, dia)
                    for x in range(0, 51):
                        siguiente_semana = timedelta(weeks=x)
                        fecha = next_dia + siguiente_semana
                        nueva_cita = Cita(Agencia=agencia,
                                          Atiende=request.user,
                                          Hora=hora, Fecha=fecha,
                                          Descripcion=agencia.get_Marca_display())
                        nueva_cita.save()
            return HttpResponseRedirect('/comercial/calendario/')
        else:
            return render(request, 'comercial/form_wdate.html', {
                                                        'form': citaform})
    citaform = CitaAgenciaForm(user=request.user)
    return render(request, 'comercial/form_wdate.html', {'form': citaform})

# ------------------------------ Views Casos -------------------------------


@login_required
@user_passes_test(comercial_check)
def nuevo_caso(request, pk_cliente):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        atiende = user
        cliente = Cliente.objects.get(pk=pk_cliente, Atiende=atiende)
    else:
        cliente = Cliente.objects.get(pk=pk_cliente)
    Eq_Solicitado_FormSet = formset_factory(Equipo_SolicitadoForm, extra=1)
    if request.method == "POST":
        caso_form = Caso_CVForm(request.POST, instance=Caso(),
                                user=user, cliente=cliente)
        formset = Eq_Solicitado_FormSet(request.POST)
        if caso_form.is_valid():
            nuevo_caso = caso_form.save(commit=False)
            nuevo_caso.Cliente = cliente
            nuevo_caso.Atiende = cliente.Atiende
            monto = 0
            nuevo_caso.Monto = monto
            nuevo_caso.save()
            for form in formset:
                if form.is_valid():
                    nuevo_eq = form.save(commit=False)
                    nuevo_eq.Caso = nuevo_caso
                    nuevo_eq.save()
                    monto = monto + nuevo_eq.Precio
            nuevo_caso.Monto = monto
            nuevo_caso.save()
            if cliente.Status == 'CA' or cliente.Status == 'CI':
                cliente.Status == 'CP'
            else:
                cliente.Status == 'PR'
            cliente.save()
            url = reverse('detalle_caso', kwargs={'pk': nuevo_caso.pk})
            return HttpResponseRedirect(url)
    caso_form = Caso_CVForm(user=user, cliente=cliente)
    return render(request, 'comercial/nuevo_caso.html',
                  {'form': caso_form,
                   'Eq_Solicitado_FormSet': Eq_Solicitado_FormSet})


@login_required
@user_passes_test(comercial_check)
def actualizar_caso(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        caso = Caso.objects.get(pk=pk, Atiende=user)
    elif user.groups.filter(name='comercial_mger').exists():
        caso = get_object_or_404(Caso, pk=pk)
    cliente = caso.Cliente
    casoform = Caso_CVForm(user=user, cliente=cliente, instance=caso)
    if request.method == "POST":
        casoform = Caso_CVForm(request.POST,
                               user=user, cliente=cliente, instance=caso)
        if casoform.is_valid():
            caso = casoform.save(commit=False)
            if caso.tracker.has_changed('Etapa'):
                if caso.Etapa == 'crd':
                    prev = caso.tracker.previous('Etapa')
                    if prev != 'fon' or prev != 'pir':
                        return Http404
                historial = Historial_Etapa(Caso=caso, Etapa=caso.Etapa)
                historial.save()
            if caso.Etapa == 'prd' or caso.Etapa == 'rzo':
                caso.Activo = False
            caso.save()
            url = reverse('detalle_caso', kwargs={'pk': caso.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/form.html', {'form': casoform, })
    return render(request, 'comercial/form.html', {'form': casoform, })


@login_required
@user_passes_test(comercial_check)
def detalle_caso(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        caso = Caso.objects.get(pk=pk, Atiende=user)
        caso.Requiere_revision_vtas = False
        caso.save()
    else:
        caso = Caso.objects.get(pk=pk)
    try:
        comprador = Contacto_C.objects.filter(
                        Cliente=caso.Cliente.pk, Rol='CM').order_by('-id')[0]
    except IndexError:
        comprador = None
    try:
        historial = Historial_Etapa.objects.filter(
                                                Caso=caso).order_by('-Fecha')
    except ObjectDoesNotExist:
        pass
    try:
        interacciones = Interaccion.objects.filter(
                                            del_Caso=caso).order_by('-Fecha')
    except ObjectDoesNotExist:
        pass
    try:
        anotaciones = Anotacion.objects.filter(al_Caso=caso).order_by('-Fecha')
    except ObjectDoesNotExist:
        pass
    try:
        eqs = Equipo_Solicitado.objects.filter(Caso=caso)
    except ObjectDoesNotExist:
        pass
    context = {'caso': caso, 'interacciones': interacciones,
               'anotaciones': anotaciones, 'historial': historial,
               'eqs': eqs, }
    return render(request, 'comercial/detalle_caso.html', context)


@login_required
@user_passes_test(comercial_check)
def lista_casos(request, etapa):
    user = request.user
    if etapa == 'crd' or etapa == 'prd' or etapa == 'rzo':
        if user.groups.filter(name='comercial_vendedor').exists():
            historial_cs = Historial_Etapa.objects.filter(
                                            Caso__Atiende=user, Etapa=etapa
                                            ).order_by('-Fecha')
        else:
            historial_cs = Historial_Etapa.objects.filter(Etapa=etapa)
        return render(request, 'comercial/lista_casos_e.html',
                      {'historial_cs': historial_cs, 'status': etapa, })
    elif user.groups.filter(name='comercial_vendedor').exists():
        casos = Caso.objects.filter(Atiende=user, Etapa=etapa)
    else:
        casos = Caso.objects.filter(Etapa=etapa)
    return render(request, 'comercial/lista_casos_d.html',
                  {'casos': casos, 'status': etapa, })


class CasoDelete(DeleteView):
    model = Caso
    template_name = 'comercial/confirm_delete.html'
    success_url = reverse_lazy('redirect')

    def get_object(self, queryset=None):
        """ Hook to ensure object owner is request.user """
        caso = super(CasoDelete, self).get_object()
        if not caso.Atiende == self.request.user and caso.Etapa == 'int':
            raise Http404
        return caso


@login_required
@user_passes_test(comercial_check)
def agregar_eq(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        caso = Caso.objects.get(pk=pk, Atiende=user)
    else:
        caso = Caso.objects.get(pk=pk)
    Eq_FormSet = formset_factory(Equipo_SolicitadoForm, extra=1)
    if request.method == 'POST':
        formset = Eq_FormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                new_eq = form.save(commit=False)
                new_eq.Caso = caso
                new_eq.save()
                caso.Monto += new_eq.Precio
            caso.save()
            url = reverse('detalle_caso', kwargs={'pk': caso.pk})
            return HttpResponseRedirect(url)
    else:
        return render(request, 'comercial/nuevo_eq.html',
                      {'formset': Eq_FormSet, })


@login_required
@user_passes_test(comercial_check)
def actualizar_eq(request, pk):
    user = request.user
    eq = Equipo_Solicitado.objects.get(pk=pk)
    if user.groups.filter(name='comercial_vendedor').exists():
        if not user == eq.Caso.Atiende:
            raise Http404
    if request.method == "POST":
        modified_eq_form = Equipo_SolicitadoForm(request.POST, instance=eq)
        if modified_eq_form.is_valid():
            caso = Caso.objects.get(pk=eq.Caso.pk)
            caso.Monto -= eq.Precio
            modified_eq = modified_eq_form.save()
            caso.Monto += modified_eq.Precio
            caso.save()
            url = reverse('detalle_caso', kwargs={'pk': eq.Caso.pk})
            return HttpResponseRedirect(url)
    else:
        form = Equipo_SolicitadoForm(instance=eq)
        return render(request, 'comercial/form.html', {'form': form, })


class Equipo_Delete(DeleteView):
    model = Equipo_Solicitado
    template_name = 'comercial/confirm_delete.html'
    success_url = reverse_lazy('redirect')

    def get_object(self, queryset=None):
        """ Hook to ensure object owner is request.user """
        eq = super(Equipo_Delete, self).get_object()
        if not eq.Caso.Atiende == self.request.user:
            raise Http404
        caso = Caso.objects.get(pk=eq.Caso.pk)
        caso.Monto -= eq.Precio
        return eq


@login_required
@user_passes_test(comercial_check)
def agregar_interaccion(request, pk_caso):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        caso = Caso.objects.get(pk=pk_caso, Atiende=user)
    elif user.groups.filter(name='comercial_mger').exists():
        caso = get_object_or_404(Caso, pk=pk_caso)
    if request.method == "POST":
        interaccionform = InteraccionForm(request.POST)
        caso_statusform = Caso_StatusForm(
                                        request.POST, instance=caso, user=user)
        if interaccionform.is_valid() and caso_statusform.is_valid():
            nueva_interaccion = interaccionform.save(commit=False)
            nueva_interaccion.Hecha_por = user
            nueva_interaccion.del_Caso = caso
            nueva_interaccion.Numero = Interaccion.objects.filter(
                                                    del_Caso=caso).count() + 1
            nuevo_caso_status = caso_statusform.save(commit=False)
            if nuevo_caso_status.tracker.has_changed('Etapa'):
                historial = Historial_Etapa(
                                    Caso=caso, Etapa=nuevo_caso_status.Etapa)
                historial.save()
                if nuevo_caso_status.Etapa == 'prd':
                    nuevo_caso_status.Activo = False
                    casos_cliente = Caso.objects.filter(Cliente=caso.Cliente)
                    x = casos_cliente.count() - 1
                    if (casos_cliente.filter(Q(Etapa='prd') |
                                             Q(Etapa='rzo')).count() == x):
                        cliente = Cliente.objects.get(pk=caso.Cliente.pk)
                        cliente.Status = 'PF'
                        cliente.save()
                elif nuevo_caso_status.Etapa == 'crd':
                    cliente.Status = 'CA'
                    cliente.save()
            else:
                historial = Historial_Etapa.objects.filter(
                                                    Caso=caso).latest('Fecha')
            nueva_interaccion.Hist_Etapa = historial
            nueva_interaccion.save()
            nuevo_caso_status.save()
            return HttpResponseRedirect('/redirect/')
        else:
            return render(request, 'comercial/nueva_interaccion.html', {
                'interaccionform': interaccionform,
                'statusform': statusform, })
    interaccionform = InteraccionForm(instance=Interaccion())
    statusform = Caso_StatusForm(instance=caso, user=user)
    return render(request, 'comercial/nueva_interaccion.html', {
            'interaccionform': interaccionform, 'statusform': statusform, })


@login_required
@user_passes_test(backup_check)
def agregar_anotacion(request, pk_caso):
    caso = get_object_or_404(Caso, pk=pk_caso)
    if request.method == "POST":
        anotacionform = AnotacionForm(request.POST)
        caso_statusform = Caso_StatusForm(
                            request.POST, instance=caso, user=request.user)
        if anotacionform.is_valid() and caso_statusform.is_valid():
            nueva_anotacion = anotacionform.save(commit=False)
            nueva_anotacion.al_Caso = caso
            nueva_anotacion.Hecha_por = request.user
            nuevo_caso_status = caso_statusform.save(commit=False)
            if nuevo_caso_status.tracker.has_changed('Etapa'):
                historial = Historial_Etapa(
                                    Caso=caso, Etapa=nuevo_caso_status.Etapa)
                historial.save()
                nueva_anotacion.Hist_Etapa = historial
                nueva_anotacion.save()
                if nuevo_caso_status.Etapa == 'rzo':
                    cliente = Cliente.objects.get(
                                            pk=nuevo_caso_status.Cliente.pk)
                    cliente.Status = 'PF'
                    cliente.save()
            else:
                historial = Historial_Etapa.objects.filter(
                                                    Caso=caso).latest('Fecha')
                nueva_anotacion.Hist_Etapa = historial
                nueva_anotacion.save()
            nuevo_caso_status.Requiere_revision_vtas = True
            nuevo_caso_status.save()
            url = reverse('detalle_caso', kwargs={'pk': caso.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/nueva_interaccion.html', {
                'interaccionform': anotacionform, 'statusform': statusform, })
    anotacionform = AnotacionForm(instance=Anotacion())
    statusform = Caso_StatusForm(instance=caso, user=request.user)
    return render(request, 'comercial/nueva_interaccion.html', {
                'interaccionform': anotacionform, 'statusform': statusform, })


def solicitar_revision(request):
    caso_pk = request.GET.get('caso_pk', None)
    if caso_pk:
        caso = get_object_or_404(Caso, pk=int(caso_pk))
        if caso.Requiere_revision_admon is True:
            return HttpResponse('Ya solicitaste revision')
        else:
            caso.Requiere_revision_admon = True
            caso.save()
        return HttpResponse('Revision solicitada')
    return HttpResponse('Error')


def revision_realizada(request):
    caso_pk = request.GET.get('caso_pk', None)
    if caso_pk:
        caso = get_object_or_404(Caso, pk=int(caso_pk))
        caso.Requiere_revision_admon = False
        caso.save()
        return HttpResponse('Gracias')
    return HttpResponse('Error')

# ------------------------------- Views Agencias ------------------------------


@login_required
@user_passes_test(comercial_check)
def nueva_agencia(request):
    user = request.user
    ContactoAFormSet = formset_factory(Contacto_Agencia_IniForm, extra=1)
    if request.method == "POST":
        if user.groups.filter(name='comercial_vendedor').exists():
            agencia_form = Agencia_AutomotrizVForm(
                                request.POST, instance=Agencia_Automotriz())
        elif (user.groups.filter(name='comercial_backup').exists()
              or user.groups.filter(name='comercial_mger').exists()):
            agencia_form = Agencia_AutomotrizForm(
                                request.POST, instance=Agencia_Automotriz())
        formset = ContactoAFormSet(request.POST)
        if agencia_form.is_valid():
            if user.groups.filter(name='comercial_vendedor').exists():
                new_agencia = agencia_form.save(commit=False)
                new_agencia.Atiende = user
                new_agencia.save()
            elif (user.groups.filter(name='comercial_backup').exists()
                  or user.groups.filter(name='comercial_mger').exists()):
                new_agencia = agencia_form.save()
            if formset.is_valid():
                for form in formset:
                    new_form = form.save(commit=False)
                    new_form.Atiende = new_agencia.Atiende
                    new_form.Agencia = new_agencia
                    new_form.save()
                return HttpResponseRedirect('/comercial/lista_agencias/')
        else:
            return render(request, 'comercial/nueva_agencia.html', {
                'agencia_form': agencia_form, 'formset': ContactoAFormSet, })
    if user.groups.filter(name='comercial_vendedor').exists():
        agencia_form = Agencia_AutomotrizVForm(instance=Agencia_Automotriz())
    elif (user.groups.filter(name='comercial_backup').exists()
          or user.groups.filter(name='comercial_mger').exists()):
        agencia_form = Agencia_AutomotrizForm(instance=Agencia_Automotriz())
        agencia_form.fields['Atiende'].queryset = User.objects.filter(
                                            groups__name='comercial_vendedor')
    else:
        return Http404
    return render(request, 'comercial/nueva_agencia.html', {
                'agencia_form': agencia_form, 'formset': ContactoAFormSet, })


@login_required
def lista_agencias(request):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        lista_agencias = Agencia_Automotriz.objects.filter(
                                                Atiende=user).order_by('Marca')
    else:
        lista_agencias = Agencia_Automotriz.objects.all().order_by('Marca')
    paginator = Paginator(lista_agencias, 20)
    page = request.GET.get('page')
    try:
        agencias = paginator.page(page)
    except PageNotAnInteger:
        agencias = paginator.page(1)
    except EmptyPage:
        agencias = paginator.page(paginator.num_pages)
    return render(request, 'comercial/lista_agencias.html', {
                                                    'agencias': agencias, })


@login_required
def actualizar_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        agencia = Agencia_Automotriz.objects.get(pk=pk, Atiende=user)
        agenciaform = Agencia_AutomotrizVForm(instance=agencia)
    elif user.groups.filter(name='comercial_mger').exists():
        agencia = get_object_or_404(Agencia_Automotriz, pk=pk)
        agenciaform = Agencia_AutomotrizForm(instance=agencia)
    else:
        return Http404
    if request.method == "POST":
        if user.groups.filter(name='comercial_vendedor').exists():
            agenciaform = Agencia_AutomotrizVForm(
                                            request.POST, instance=agencia)
        elif user.groups.filter(name='comercial_mger').exists():
            agenciaform = Agencia_AutomotrizForm(
                                            request.POST, instance=agencia)
        if agenciaform.is_valid():
            agencia = agenciaform.save()
            url = reverse('detalle_agencia', kwargs={'pk': agencia.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/form.html', {
                                                    'form': agenciaform, })
    return render(request, 'comercial/form.html', {'form': agenciaform, })


@login_required
def detalle_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        try:
            agencia = Agencia_Automotriz.objects.get(pk=pk, Atiende=user)
        except ObjectDoesNotExist:
            raise Http404
    elif (user.groups.filter(name='comercial_mger').exists()
          or user.groups.filter(name='comercial_backup').exists()):
        agencia = get_object_or_404(Agencia_Automotriz, pk=pk)
    try:
        contactos = Contacto_Agencia.objects.filter(
                        Agencia=agencia).order_by('Rol', 'Nombre_del_Contacto')
    except ObjectDoesNotExist:
        pass
    try:
        cuentas = Cuenta_Bancaria.objects.filter(Agencia=agencia)
    except ObjectDoesNotExist:
        pass
    return render(request, 'comercial/detalle_agencia.html', {
            'agencia': agencia, 'contactos': contactos, 'cuentas': cuentas, })


class AgenciaDelete(DeleteView):
    model = Agencia_Automotriz
    template_name = 'comercial/confirm_delete.html'
    success_url = reverse_lazy('lista_agencias')

    def get_object(self, queryset=None):
        """ Hook to ensure object owner is request.user """
        agencia = super(AgenciaDelete, self).get_object()
        if not agencia.Atiende == self.request.user:
            raise Http404
        return agencia


@login_required
@user_passes_test(comercial_check)
def lista_casos_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        agencia = Agencia_Automotriz.objects.get(pk=pk, Atiende=user)
    else:
        agencia = Agencia_Automotriz.objects.get(pk=pk)
    casos = Caso.objects.filter(Agencia=agencia,
                                Etapa__in=['int', 'cot', 'epa', 'eap', 'apr',
                                           'cfr', 'pir', 'fon']
                                ).order_by('Etapa')
    hists_estaticos = Historial_Etapa.objects.filter(Caso__Agencia=agencia,
                                                     Etapa__in=['crd',
                                                                'prd',
                                                                'rzo']
                                                     ).order_by('Fecha')
    return render(request, 'comercial/lista_casos_vendedor.html',
                  {'agencia': agencia, 'casos': casos,
                   'hists_estaticos': hists_estaticos, })


@login_required
@user_passes_test(comercial_check)
def nuevo_contacto_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        agencia = Agencia_Automotriz.objects.get(pk=pk, Atiende=user)
    elif (user.groups.filter(name='comercial_mger').exists()
          or user.groups.filter(name='comercial_backup').exists()):
        agencia = get_object_or_404(Agencia_Automotriz, pk=pk)
    ContactoAFormSet = formset_factory(Contacto_Agencia_IniForm, extra=1)
    if request.method == 'POST':
        formset = ContactoAFormSet(request.POST)
        for form in formset:
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.Atiende = agencia.Atiende
                new_form.Agencia = agencia
                new_form.save()
            else:
                print("Form is not valid")
        url = reverse('detalle_agencia', kwargs={'pk': agencia.pk})
        return HttpResponseRedirect(url)
    return render(request, 'comercial/nuevo_contacto_agencia.html', {
                                                'formset': ContactoAFormSet, })


@login_required
def editar_contacto_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        contacto = Contacto_Agencia.objects.get(pk=pk, Atiende=user)
    elif user.groups.filter(name='comercial_mger').exists(
                ) or user.groups.filter(name='comercial_backup').exists():
        contacto = get_object_or_404(Contacto_Agencia, pk=pk)
    if request.method == 'POST':
        contactoform = Contacto_Agencia_IniForm(
                                            request.POST, instance=contacto)
        if contactoform.is_valid():
            contacto = contactoform.save()
            url = reverse('lista_agencias',)
            return HttpResponseRedirect(url)
    contactoform = Contacto_Agencia_IniForm(instance=contacto)
    return render(request, 'comercial/form.html', {'form': contactoform, })


@login_required
def lista_casos_vendedor_agencia(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        contacto = Contacto_Agencia.objects.get(pk=pk, Atiende=user)
    elif user.groups.filter(name='comercial_mger').exists():
        contacto = get_object_or_404(Contacto_Agencia, pk=pk)
    else:
        return Http404
    lista_casos = Caso.objects.filter(
                                Vendedor_Agencia=contacto).order_by('Etapa')
    paginator = Paginator(lista_casos, 10)
    page = request.GET.get('page')
    try:
        casos = paginator.page(page)
    except PageNotAnInteger:
        casos = paginator.page(1)
    except EmptyPage:
        casos = paginator.page(paginator.num_pages)
    return render(request, 'comercial/lista_casos_vendedor.html', {
                                'contacto': contacto, 'casos': casos, })


@login_required
def lista_vendedores_agencia(request):
    user = request.user
    # Adjust queryset according to parameters
    if user.groups.filter(name='comercial_vendedor').exists():
        lista_vendedores = Contacto_Agencia.objects.filter(
                                Atiende=user).order_by("Nombre_del_Contacto")
    else:
        lista_vendedores = Contacto_Agencia.objects.filter.all(
                                            ).order_by("Nombre_del_Contacto")
    query = request.GET.get("q")
    if query:
        lista_vendedores = lista_vendedores.filter(
                Q(Nombre_del_Contacto__icontains=query) |
                Q(Celular__icontains=query) |
                Q(Rol__icontains=query)
        ).distinct()
    # Paginator
    paginator = Paginator(lista_vendedores, 20)
    page = request.GET.get('page')
    try:
        vendedores = paginator.page(page)
    except PageNotAnInteger:
        vendedores = paginator.page(1)
    except EmptyPage:
        vendedores = paginator.page(paginator.num_pages)
    context = {'vendedores': vendedores, }
    return render(request, 'comercial/lista_vendedores.html', context)


class Contacto_AgenciaDelete(DeleteView):
    model = Contacto_Agencia
    template_name = 'comercial/confirm_delete.html'
    success_url = reverse_lazy('lista_agencias')

    def get_object(self, queryset=None):
        """ Hook to ensure object owner is request.user """
        contacto = super(Contacto_AgenciaDelete, self).get_object()
        if not contacto.Atiende == self.request.user:
            raise Http404
        return contacto

# ------------------------------- Views Clientes ------------------------------
# Crea un objeto Cliente y un objeto Caso


@login_required
@user_passes_test(comercial_check)
def nuevo_prospecto(request):
    user = request.user
    Eq_Solicitado_FormSet = formset_factory(Equipo_SolicitadoForm, extra=1)
    if request.method == "POST":
        if user.groups.filter(name='comercial_vendedor').exists():
            clienteform = Cliente_VForm(request.POST, instance=Cliente())
        elif user.groups.filter(name='comercial_backup').exists(
                    ) or user.groups.filter(name='comercial_mger').exists():
            clienteform = ClienteForm(request.POST, instance=Cliente())
        contacto_cform = Contacto_CCAForm(request.POST, instance=Contacto_C())
        caso_form = Caso_IniForm(request.POST, instance=Caso(), user=user)
        formset = Eq_Solicitado_FormSet(request.POST)
        if clienteform.is_valid() and contacto_cform.is_valid(
                                ) and caso_form.is_valid(
                                ) and formset.is_valid():
            nuevo_cliente = clienteform.save(commit=False)
            if user.groups.filter(name='comercial_vendedor').exists():
                nuevo_cliente.Atiende = request.user
            nuevo_cliente.Status = 'PR'
            nuevo_cliente.save()
            nuevo_contacto = contacto_cform.save(commit=False)
            nuevo_contacto.Cliente = nuevo_cliente
            nuevo_contacto.Atiende = nuevo_cliente.Atiende
            nuevo_contacto.save()
            nuevo_caso = caso_form.save(commit=False)
            nuevo_caso.Atiende = nuevo_cliente.Atiende
            nuevo_caso.Cliente = nuevo_cliente
            nuevo_caso.Contacto = nuevo_contacto
            nuevo_caso.Activo = True
            monto = 0
            nuevo_caso.Monto = monto
            nuevo_caso.save()
            historial = Historial_Etapa(
                                    Caso=nuevo_caso, Etapa=nuevo_caso.Etapa)
            historial.save()
            for eq in formset:
                new_eq = eq.save(commit=False)
                new_eq.Caso = nuevo_caso
                new_eq.save()
                monto = monto + new_eq.Precio
            nuevo_caso.Monto = monto
            nuevo_caso.save()
            url = reverse('redirect')
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/crear_prospecto.html', {
                'clienteform': clienteform, 'contacto_cform': contacto_cform,
                'caso_form': caso_form, })
    contacto_cform = Contacto_CCAForm()
    caso_form = Caso_IniForm(user=user)
    if user.groups.filter(name='comercial_vendedor').exists():
        clienteform = Cliente_VForm()
    elif user.groups.filter(name='comercial_backup').exists(
                    ) or user.groups.filter(name='comercial_mger').exists():
        clienteform = ClienteForm()
    else:
        return Http404
    return render(request, 'comercial/crear_prospecto.html', {
                           'clienteform': clienteform,
                           'contacto_cform': contacto_cform,
                           'caso_form': caso_form,
                           'Eq_Solicitado_FormSet': Eq_Solicitado_FormSet})


@login_required
def editar_cliente(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        cliente = Cliente.objects.get(pk=pk, Atiende=user)
        clienteform = Cliente_VForm(instance=cliente)
    elif user.groups.filter(name='comercial_mger').exists(
                    ) or user.groups.filter(name='comercial_backup').exists():
        cliente = get_object_or_404(Cliente, pk=pk)
        clienteform = Cliente_Form(instance=cliente)
    else:
        return Http404
    if request.method == "POST":
        if user.groups.filter(name='comercial_vendedor').exists(
                    ) or user.groups.filter(name='comercial_backup').exists():
            clienteform = Cliente_VForm(request.POST, instance=cliente)
        elif user.groups.filter(name='comercial_mger').exists():
            clienteform = Cliente_Form(request.POST, instance=cliente)
        if clienteform.is_valid():
            cliente = clienteform.save()
            url = reverse('detalle_cliente', kwargs={'pk': cliente.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/actualizar.html', {
                                                        'objeto': cliente, })
    return render(request, 'comercial/form.html', {'form': clienteform, })


@login_required
def lista_clientes(request, vendedor_pk, status, tipo):
    user = request.user
    # Adjust queryset according to parameters
    if user.groups.filter(name='comercial_vendedor').exists():
        if status == 'AL':
            lista_clientes = Cliente.objects.filter(Atiende=request.user)
        else:
            lista_clientes = Cliente.objects.filter(
                                        Atiende=request.user, Status=status)
    elif vendedor_pk == '000':
        if status == 'AL':
            lista_clientes = Cliente.objects.all()
        else:
            lista_clientes = Cliente.objects.filter(Status=status)
    else:
        if status == 'AL':
            lista_clientes = Cliente.objects.filter(Atiende=vendedor_pk)
        else:
            lista_clientes = Cliente.objects.filter(
                                        Atiende=vendedor_pk, Status=status)
    query = request.GET.get("q")
    if query:
        lista_clientes = lista_clientes.filter(
                Q(RFC__icontains=query) |
                Q(Nombre_Empresa__icontains=query) |
                Q(Industria__icontains=query)
        ).distinct()
    # Paginator
    paginator = Paginator(lista_clientes, 20)
    page = request.GET.get('page')
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(1)
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)
    if tipo == 'L':
        context = {'clientes': clientes, 'titulo': 'Lista de Clientes:',
                   'c_link': 'detalle', }
        return render(request, 'comercial/lista_clientes.html', context)
    elif tipo == 'S':
        context = {'clientes': clientes, 'titulo': 'Selecciona un Cliente:',
                   'c_link': 'nuevo_caso', }
        return render(request, 'comercial/lista_clientes.html', context)
    else:
        return Http404


@login_required
def detalle_cliente(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        cliente = get_object_or_404(Cliente, pk=pk, Atiende=request.user)
    else:
        cliente = get_object_or_404(Cliente, pk=pk)
    try:
        direccion = Direccion_Fiscal_Cliente.objects.get(Cliente=cliente)
    except ObjectDoesNotExist:
        direccion = None
    contactos = Contacto_C.objects.filter(Cliente=cliente)
    contratos = Contrato.objects.filter(Cliente=cliente)
    anexos = Anexo.objects.filter(Cliente=cliente)
    facturas = Factura.objects.filter(Cliente=cliente)
    context = {'cliente': cliente, 'direccion': direccion,
               'contactos': contactos, 'contratos': contratos,
               'anexos': anexos, 'facturas': facturas, }
    return render(request, 'comercial/detalle_cliente.html', context)

# --------------------------- Views Contacto clientes ------------------------


@login_required
def nuevo_contacto(request, pk):
    user = request.user
    if request.method == "POST":
        if pk != '000':
            if user.groups.filter(name='comercial_vendedor').exists():
                cliente = Cliente.objects.get(pk=pk, Atiende=user)
            else:
                cliente = Cliente.objects.get(pk=pk)
            contactoform = Contacto_CCAForm(request.POST)
            if contactoform.is_valid():
                nuevo_contacto = contactoform.save(commit=False)
                nuevo_contacto.Atiende = cliente.Atiende
                nuevo_contacto.Cliente = cliente
            else:
                return render(request, 'comercial/form_wdate.html', {
                                                    'form': contactoform, })
        else:
            if user.groups.filter(name='comercial_vendedor').exists():
                contactoform = Contacto_CCForm(request.POST, user=user)
                if contactoform.is_valid():
                    nuevo_contacto = contactoform.save(commit=False)
                    nuevo_contacto.Atiende = user
                else:
                    return render(request, 'comercial/form_wdate.html', {
                                                    'form': contactoform, })
            else:
                contactoform = Contacto_CForm(request.POST)
                if contactoform.is_valid():
                    nuevo_contacto = contactoform.save(commit=False)
                else:
                    return render(request, 'comercial/form_wdate.html', {
                                                    'form': contactoform, })
            cliente = nuevo_contacto.Cliente
        nuevo_contacto.save()
        url = reverse('detalle_cliente', kwargs={'pk': cliente.pk})
        return HttpResponseRedirect(url)
    if pk != '000':
        if user.groups.filter(name='comercial_vendedor').exists():
            cliente = Cliente.objects.get(pk=pk, Atiende=user)
        contactoform = Contacto_CCAForm()
    else:
        if user.groups.filter(name='comercial_vendedor').exists():
            contactoform = Contacto_CCForm(user=user)
        else:
            contactoform = Contacto_CForm()
    return render(request, 'comercial/form_wdate.html', {
                                                    'form': contactoform, })


@login_required
@user_passes_test(comercial_check)
def editar_contacto(request, pk):
    user = request.user
    contacto = get_object_or_404(Contacto_C, pk=pk)
    if user.groups.filter(name='comercial_vendedor').exists():
        cliente = Cliente.objects.get(
                            Nombre_Empresa=contacto.Cliente, Atiende=user)
    contactoform = Contacto_CCForm(instance=contacto, user=user)
    if request.method == "POST":
        contactoform = Contacto_CCForm(
                            request.POST, instance=contacto, user=user)
        if contactoform.is_valid():
            contacto = contactoform.save()
            url = reverse('detalle_contacto', kwargs={'pk': contacto.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/form.html', {
                                                    'form': contactoform, })
    return render(request, 'comercial/form.html', {'form': contactoform, })


@login_required
def detalle_contacto(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        contacto = Contacto_C.objects.get(pk=pk, Atiende=user)
    else:
        contacto = Contacto_C.objects.get(pk=pk)
    return render(request, 'comercial/detalle_contacto_cliente.html', {
                                                    'contacto': contacto, })

# ----------------------------- Views Direccion clientes --------------------


@login_required
def nueva_direccion(request, pk):
    user = request.user
    if not pk == '000':
        try:
            direccion = Direccion_Fiscal_Cliente.objects.get(Cliente=pk)
            url = reverse('detalle_direccion', kwargs={'pk': direccion.pk})
            return HttpResponseRedirect(url)
        except ObjectDoesNotExist:
            if user.groups.filter(name='comercial_vendedor').exists():
                cliente = Cliente.objects.get(pk=pk, Atiende=user)
            else:
                cliente = get_object_or_404(Cliente, pk=pk)
            direccionform = Direccion_Fiscal_ClienteCForm()
    else:
        direccionform = Direccion_Fiscal_ClienteForm()
    if request.method == "POST":
        if not pk == '000':
            direccionform = Direccion_Fiscal_ClienteCForm(request.POST)
            if direccionform.is_valid():
                nueva_direccion = direccionform.save(commit=False)
                nueva_direccion.Cliente = cliente
                nueva_direccion.save()
            else:
                return render(request, 'comercial/form_wdate.html', {
                                                    'form': direccionform, })
        else:
            form = Direccion_Fiscal_ClienteForm(request.POST)
            if direccionform.is_valid():
                nueva_direccion = direccionform.save()
            else:
                return render(request, 'comercial/form_wdate.html', {
                                                    'form': direccionform, })
    return render(request, 'comercial/form_wdate.html', {
                                                    'form': direccionform, })


@login_required
def editar_direccion(request, pk):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').exists():
        direccion = get_object_or_404(Direccion_Fiscal_Cliente, pk=pk)
        cliente = Cliente.objects.get(
                            Nombre_Empresa=direccion.Cliente, Atiende=user)
        direccionform = Direccion_Fiscal_ClienteCForm(instance=direccion)
    elif user.groups.filter(name='comercial_backup').exists(
                    ) or user.groups.filter(name='comercial_mger').exists():
        direccion = get_object_or_404(Direccion_Fiscal_Cliente, pk=pk)
        direccionform = Direccion_Fiscal_ClienteForm(instance=direccion)
    else:
        return Http404
    if request.method == "POST":
        if user.groups.filter(name='comercial_vendedor').exists():
            direccionform = Direccion_Fiscal_ClienteCForm(
                                        request.POST, instance=direccion)
        elif user.groups.filter(name='comercial_backup').exists(
                    ) or user.groups.filter(name='comercial_mger').exists():
            direccionform = Direccion_Fiscal_ClienteForm(
                                        request.POST, instance=direccion)
        if direccionform.is_valid():
            direccion = direccionform.save()
            url = reverse('detalle_direccion', kwargs={'pk': direccion.pk})
            return HttpResponseRedirect(url)
        else:
            return render(request, 'comercial/form.html', {
                                                'form': direccionform, })
    return render(request, 'comercial/form.html', {
                                                'form': direccionform, })

# ---------------------------- Views Documentacion -----------------------


@login_required
@user_passes_test(backup_check)
def nueva_documentacion_caso(request, pk_caso):
    caso = get_object_or_404(Caso, pk=pk_caso)
    if request.method == "POST":
        if caso.Cliente.Persona_Moral is True:
            docuform = Documentacion_PMoral_Form(request.POST)
        else:
            docuform = Documentacion_PFisica_Form(request.POST)
        if docuform.is_valid():
            nueva_documentacion = docuform.save(commit=False)
            nueva_documentacion.Caso = caso
            nueva_documentacion.save()
            url = reverse('redirect')
            return HttpResponseRedirect(url)
    if caso.Cliente.Persona_Moral is True:
        docuform = Documentacion_PMoral_Form()
    else:
        docuform = Documentacion_PFisica_Form()
    return render(request, 'comercial/docuform.html', {'docuform': docuform, })


@login_required
@user_passes_test(backup_check)
def actualizar_documentacion_caso(request, pk, tipo):
    if tipo == 'M':
        documentacion = get_object_or_404(Documentacion_PMoral, pk=pk)
    elif tipo == 'F':
        documentacion = get_object_or_404(Documentacion_PFisica, pk=pk)
    if request.method == "POST":
        if tipo == 'M':
            docuform = Documentacion_PMoral_Form(
                                    request.POST, instance=documentacion)
        elif tipo == 'F':
            docuform = Documentacion_PFisica_Form(
                                    request.POST, instance=documentacion)
        if docuform.is_valid():
            nueva_documentacion = docuform.save()
            url = reverse('redirect')
            return HttpResponseRedirect(url)
    if tipo == 'M':
        docuform = Documentacion_PMoral_Form(instance=documentacion)
    elif tipo == 'F':
        docuform = Documentacion_PFisica_Form(instance=documentacion)
    return render(request, 'comercial/docuform.html', {
                                                'docuform': docuform, })

# ------------------------------ Views Calendario ---------------------------


def calendario(request):
    hoy = date.today()
    citas = Cita.objects.filter(Atiende=request.user, Fecha__year=hoy.year,
                                Fecha__month=hoy.month).order_by('Fecha')
    seguimientos = Interaccion.objects.filter(Hecha_por=request.user,
                                              Buscar_el__year=hoy.year,
                                              Buscar_el__month=hoy.month
                                              ).order_by('Buscar_el')
    casos = Caso.objects.filter(Atiende=request.user, Buscar_el__year=hoy.year,
                                Buscar_el__month=hoy.month,
                                Activo=True).order_by('Buscar_el')
    mis_citas = list(chain(citas, seguimientos, casos))
    cal = AgendaCalendar(mis_citas).formatmonth(hoy.year, hoy.month)
    next_month = hoy + relativedelta(months=+1)
    previous_month = hoy + relativedelta(months=-1)
    context = {'calendar': mark_safe(cal),
               'next_month': next_month.strftime("%B"),
               'previous_month': previous_month.strftime("%B"),
               'n_month': next_month, 'p_month': previous_month, }
    return render(request, 'comercial/calendar.html', context)


def calendario_t(request, ano, mes):
    ano = int(ano)
    mes = int(mes)
    fecha = date.today()
    fecha = fecha.replace(year=ano, month=mes)
    citas = Cita.objects.filter(Atiende=request.user, Fecha__year=fecha.year,
                                Fecha__month=fecha.month).order_by('Fecha')
    seguimientos = Interaccion.objects.filter(Hecha_por=request.user,
                                              Buscar_el__year=fecha.year,
                                              Buscar_el__month=fecha.month
                                              ).order_by('Buscar_el')
    casos = Caso.objects.filter(Atiende=request.user,
                                Buscar_el__year=fecha.year,
                                Buscar_el__month=fecha.month,
                                Activo=True).order_by('Buscar_el')
    mis_citas = list(chain(citas, seguimientos, casos))
    cal = AgendaCalendar(mis_citas).formatmonth(fecha.year, fecha.month)
    next_month = fecha + relativedelta(months=+1)
    previous_month = fecha + relativedelta(months=-1)
    context = {'calendar': mark_safe(cal),
               'next_month': next_month.strftime("%B"),
               'previous_month': previous_month.strftime("%B"),
               'n_month': next_month, 'p_month': previous_month, }
    return render(request, 'comercial/calendar.html', context)


def detalle_cita(request):
    cita_pk = request.GET.get('cita_pk', None)
    if cita_pk:
        cita = get_object_or_404(Cita, pk=int(cita_pk))
        if cita.Cliente:
            try:
                comprador = Contacto_C.objects.filter(
                                        Cliente=cita.Cliente.pk, Rol='CM'
                                        ).order_by('-id')[0]
            except IndexError:
                comprador = None
            url = cita.Cliente.get_absolute_url()
            return HttpResponse('<p><a href="' + url + '">' +
                                cita.Cliente.Nombre_Empresa + '</a></p>'
                                '<p>Descripcion: ' + cita.Descripcion + '</p>'
                                '<p>El ' + str(cita.Fecha) + ' a las: ' +
                                str(cita.Hora) + '</p><p>' +
                                comprador.Nombre_del_Contacto + ' | ' +
                                comprador.Celular + ' | <a href="mailto:' +
                                comprador.Email + '">' + comprador.Email +
                                '</a></p>')
        elif cita.Agencia:
            url = cita.Agencia.get_absolute_url()
            return HttpResponse('<p><a href="' + url + '">' +
                                cita.Agencia.get_Marca_display() + ' | ' +
                                cita.Agencia.Colonia + '</a></p>'
                                '<p>El ' + str(cita.Fecha) + ' a las: ' +
                                str(cita.Hora) + '</p>')
    return HttpResponse('Error')


def detalle_interaccion(request):
    inte_pk = request.GET.get('inte_pk', None)
    if inte_pk:
        inte = get_object_or_404(Interaccion, pk=int(inte_pk))
        try:
            comprador = Contacto_C.objects.filter(
                                Cliente=inte.del_Caso.Cliente.pk, Rol='CM'
                                ).order_by('-id')[0]
        except IndexError:
            comprador = None
        url_cliente = inte.del_Caso.Cliente.get_absolute_url()
        url_caso = inte.del_Caso.get_absolute_url()
        return HttpResponse('<p><a href="' + url_cliente + '">' +
                            inte.del_Caso.Cliente.Nombre_Empresa + '</a></p>'
                            '<p><a href="' + url_caso + '">' +
                            inte.Descripcion + '</a></p><p>' +
                            comprador.Nombre_del_Contacto + ' | ' +
                            comprador.Celular + ' | <a href="mailto:' +
                            comprador.Email + '">' + comprador.Email +
                            '</a></p>')
    return HttpResponse('Error')


def detalle_caso_calendario(request):
    caso_pk = request.GET.get('caso_pk', None)
    if caso_pk:
        caso = get_object_or_404(Caso, pk=int(caso_pk))
        try:
            comprador = Contacto_C.objects.filter(
                                        Cliente=caso.Cliente.pk, Rol='CM'
                                        ).order_by('-id')[0]
        except IndexError:
            comprador = None
        url_cliente = caso.Cliente.get_absolute_url()
        return HttpResponse('<p><a href="' + url_cliente + '">' +
                            caso.Cliente.Nombre_Empresa + '</a></p>'
                            '<p>' + comprador.Nombre_del_Contacto + ' | ' +
                            comprador.Celular + ' | <a href="mailto:' +
                            comprador.Email + '">' + comprador.Email +
                            '</a></p>')
    return HttpResponse('Error')


# ------------------------------ Views Report Lab ---------------------------


@login_required
def comparativa_arr(request):
    if request.method == 'POST':
        form = ComparativaForm(request.POST)
        if form.is_valid():
            utilitario = form.cleaned_data.get('Vehiculo_de_Trabajo')
            if utilitario is True:
                return HttpResponse('Necesitas un café..')
            monto = int(form.cleaned_data.get('Monto'))
            plazo = int(form.cleaned_data.get('Plazo'))
            if form.cleaned_data.get('Aportacion_Adicional'):
                ap_adicional = int(form.cleaned_data.get(
                                                    'Aportacion_Adicional'))
            else:
                ap_adicional = 0
            competencia = form.cleaned_data.get('Contra')
            pago_inicial = int(form.cleaned_data.get('Pago_Inicial'))
            r_en_pi = int(form.cleaned_data.get(
                                'Numero_Rentas_Incluidas_en_Pago_Inicial'))
            renta = int(form.cleaned_data.get('Renta'))
            deduccion_mensual = int(form.cleaned_data.get('Deduccion_Mensual'))
            vr = int(form.cleaned_data.get('Valor_Residual'))
            fc = 0.3
            if plazo == 24:
                vr_av = 0.34
                fc = 0.39
            elif plazo == 36:
                vr_av = 0.14
            else:
                vr_av = 0.05
            renta_av = int(((monto*(1-vr_av))/((1-(1+fc/12)**(-1*plazo)) /
                            (fc/12))+50)/1.16)
            deduc_renta_av = int(renta_av*0.45+6000)
            if deduc_renta_av > renta_av:
                deduc_renta_av = renta_av
            pago_ini_av = int(((monto-(ap_adicional*0.75))*0.05 +
                               renta_av*2*1.16+ap_adicional)/1.16)
            vr_avance = int((monto*vr_av)/1.16)
            mnod_av = int((renta_av-deduc_renta_av)*(plazo-1) + vr_avance)
            mnod = int((renta-deduccion_mensual)*(plazo-r_en_pi) + vr +
                       pago_inicial)
            d_total_av = int(deduc_renta_av*(plazo-1) + pago_ini_av)
            d_total = int(deduccion_mensual*(plazo-r_en_pi) + 6000)
            return comparativaPDF(monto, plazo, ap_adicional, renta_av,
                                  deduc_renta_av, pago_ini_av, vr_avance,
                                  competencia, pago_inicial, renta,
                                  deduccion_mensual, vr, mnod_av, mnod,
                                  d_total_av, d_total)
    form = ComparativaForm()
    return render(request, 'comercial/form_comparativa.html', {'form': form, })


@login_required
@user_passes_test(backup_check)
def generar_oc(request, pk_caso):
    caso = Caso.objects.get(pk=pk_caso)
    if request.method == 'POST':
        form = OC_Form(request.POST)
        if form.is_valid():
            # Get the information for the OC
            cantidad = form.cleaned_data.get('Cantidad')
            modelo = form.cleaned_data.get('Modelo')
            color = form.cleaned_data.get('Color')
            color_interno = form.cleaned_data.get('Color_Interno')
            transmision = form.cleaned_data.get('Transmision')
            precio = form.cleaned_data.get('Precio_Unitario')
            total = str(precio * cantidad)
            today = datetime.today()
            if caso.Agencia.Nombre_Fiscal:
                Nombre_Agencia = caso.Agencia.Nombre_Fiscal
            else:
                Nombre_Agencia = "FAVOR DE LLENAR ESTA INFORMACION"
            if caso.Agencia.Calle:
                calle = caso.Agencia.Calle
            else:
                calle = "FAVOR DE LLENAR ESTA INFORMACION"
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            pdf_name = "oc.pdf"
            buff = BytesIO()
            doc = SimpleDocTemplate(buff,
                                    pagesize=letter,
                                    rightMargin=40,
                                    leftMargin=40,
                                    topMargin=60,
                                    bottomMargin=45,
                                    )
            PAGE_WIDTH = letter[0]

            # Our container for 'Flowable' objects
            elements = []

            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()

            # Set some styles for paragraphs
            styles.add(ParagraphStyle(name='RightAlign', fontSize=10,
                                      alignment=TA_RIGHT))
            styles.add(ParagraphStyle(name='CenterAlign', alignment=TA_CENTER))
            styles.add(ParagraphStyle(name='LeftAlign', alignment=TA_LEFT))
            styles.add(ParagraphStyle(name='Justified', alignment=TA_JUSTIFY))

            # Set some styles for tables
            Cuadricula = TableStyle([('GRID', (0, 0), (-1, -1), 0.25,
                                      colors.blue),
                                     ('BOX', (0, 0), (-1, -1), 0.50,
                                      colors.blue),
                                     ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                                     ('VALIGN', (0, 0), (-1, -1), 'TOP'), ])

            # Start to write document
            elements.append(Paragraph("Ciudad de Mexico a " + str(today.day) +
                                      " de " + str(today.year),
                                      styles['RightAlign']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(
                        Paragraph(
                                  "En Atencion a " +
                                  caso.Vendedor_Agencia.Nombre_del_Contacto,
                                  styles['LeftAlign']))
            elements.append(Paragraph(Nombre_Agencia, styles['LeftAlign']))
            elements.append(Paragraph(calle, styles['LeftAlign']))
            elements.append(Paragraph(caso.Agencia.Colonia + " Mexico "
                            + caso.Agencia.Ciudad, styles['LeftAlign']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("ORDEN DE COMPRA:",
                            styles['CenterAlign']))
            elements.append(Spacer(1, 0.2*inch))
            x = PAGE_WIDTH-(1.3*inch)
            colwidths = (x/9, x/1.7, x/7, x/7)
            rowheights = (0.4*inch)
            data = ((Paragraph("Cantidad", styles['LeftAlign']),
                     Paragraph("Descripcion", styles['LeftAlign']),
                     Paragraph("Precio Unitario", styles['LeftAlign']),
                     Paragraph("Precio Total", styles['LeftAlign']),),
                    (Paragraph(str(cantidad), styles['LeftAlign']),
                     Paragraph(caso.Agencia.get_Marca_display()
                               + " Modelo: " + modelo + " Color: " + color +
                               " Color Interno: " + color_interno +
                               " Transmision " + transmision
                               , styles['LeftAlign']),
                     Paragraph("$" + str(precio), styles['LeftAlign']),
                     Paragraph("$" + total, styles['LeftAlign']),),
                    )
            t = Table(data, colwidths, rowheights, hAlign='LEFT')
            t.setStyle(Cuadricula)
            elements.append(t)
            elements.append(Spacer(1, 0.4*inch))
            elements.append(Paragraph("""POR TAL MOTIVO SOLICITO NOS ENVIEEN
                 LA FACTURA ORIGINAL EN PDF, ASI COMO SU XML, ESCANEADO A LOS
                 CORREOS aurora@arrendadoraavance.com.mx,
                 alfredo@arrendadoraavance.com.mx,
                 miguel@arrendadoraavance.com.mx
                 PARA REALIZAR TRAMITES INTERNOS.""", styles['LeftAlign']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("""A RESERVA DE RECIBIR FACTURA ORIGINAL
                 CON SELLO Y FIRMA PARA REALIZAR PAGO DE LA UNIDAD.""",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("""FAVOR DE ENVIAR NUMERO DE CUENTA
                 BANCARIA Y BANCO A FIN DE DARLA DE ALTA,
                 PARA AGILIZAR PAGO. """, styles['LeftAlign']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("DE ANTEMANO GRACIAS. ",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("NUESTROS DATOS FISCALES SON:",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("Arrendadora Avance S.A. de C.V.",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("""RFC: AAV040607AA0 (AAV CERO CUATRO
                 CERO SEIS CERO SIETE AA CERO)""", styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("""CRACOVIA NO. 72 BIS INT. PO18 NIVEL 3
                 TORRE B, COL. SAN ANGEL""", styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("""DEL. ALVARO OBREGON, CIUDAD DE MEXICO,
                 C.P. 01000""", styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("""METODO DE PAGO: 03 Transferencia
                 electrónica de fondos.""", styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("CUENTA: Banorte 1400",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.4*inch))
            elements.append(Paragraph("ATENTAMENTE", styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("Carlos Miguel Rivera Romón.",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("Ejecutivo Comercial",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("Arrendadora Avance Oficina",
                            styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("6363-1990", styles['LeftAlign']))
            elements.append(Spacer(1, 0.03*inch))
            elements.append(Paragraph("miguel@arrendadoraavance.com.mx",
                            styles['LeftAlign']))
            doc.multiBuild(elements, canvasmaker=ocCanvas)
            response.write(buff.getvalue())
            buff.close()
            return response
    else:
        form = OC_Form()
        return render(request, 'comercial/form_targetb.html',
                      {'form': form, 'title': caso, })


class ocCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Pagina %s de %s" % (self._pageNumber, page_count)
        direccion1 = "Cracovia 72 BIS, PO18, Torre B, Nivel 3"
        direccion2 = "Colonia San Ángel / Álvaro Obregón 01000 / CDMX"
        direccion3 = "www.arrendadoraavance.com.mx"
        logo = '/home/django/django_project/static/avancelogo.jpg'
        self.saveState()
        self.drawImage(logo,  45, letter[1] - 70, width=1.2*inch,
                       height=0.4*inch)
        # Footer
        self.setFont('Times-Roman', 10)
        self.setFillColorRGB(0.54, 0.54, 0.54)
        self.drawString(letter[0]/2 - 40, 40, page)
        self.drawString(42, 40, direccion1)
        self.drawString(42, 30, direccion2)
        self.drawString(42, 20, direccion3)
        self.restoreState()
