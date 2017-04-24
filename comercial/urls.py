
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from comercial import views

urlpatterns = [
    #index / comercial user
    url(r'^ctrl_panel_vendedor/$', views.ctrl_panel_vendedor, name="ctrl_panel_vendedor"),
    url(r'^ctrl_panel_backup/$', views.ctrl_panel_backup, name="ctrl_panel_backup"),
    #Cliente urls
    url(r'^nuevo_prospecto/$', views.nuevo_prospecto, name="nuevo_prospecto"),
    url(r'^editar_cliente/(?P<pk>[0-9]+)/$', views.editar_cliente, name="editar_cliente"),
    url(r'^detalle_cliente/(?P<pk>[0-9]+)/$', views.detalle_cliente, name="detalle_cliente"),
    url(r'^lista_clientes/(?P<vendedor_pk>[0-9]+)/(?P<status>[A-Z]{2})/(?P<tipo>[L,S]{1})/$', views.lista_clientes, name="lista_clientes"),
    #Contacto urls
    url(r'^nuevo_contacto/(?P<pk>[0-9]+)/$', views.nuevo_contacto, name="nuevo_contacto"),
    url(r'^editar_contacto/(?P<pk>[0-9]+)/$', views.editar_contacto, name="editar_contacto"),
    #Direccion urls
    url(r'^nueva_direccion/(?P<pk>[0-9]+)/$', views.nueva_direccion, name="nueva_direccion"),
    url(r'^editar_direccion/(?P<pk>[0-9]+)/$', views.editar_direccion, name="editar_direccion"),
    #Agenica urls
    url(r'^nueva_agencia/$', views.nueva_agencia, name="nueva_agencia"),
    url(r'^lista_agencias/$', views.lista_agencias, name="lista_agencias"),
    url(r'^actualizar_agencia/(?P<pk>[0-9]+)/$', views.actualizar_agencia, name="actualizar_agencia"),
    url(r'^detalle_agencia/(?P<pk>[0-9]+)/$', views.detalle_agencia, name="detalle_agencia"),
    url(r'^nuevo_contacto_agencia/(?P<pk>[0-9]+)/$', views.nuevo_contacto_agencia, name="nuevo_contacto_agencia"),
    url(r'^editar_contacto_agencia/(?P<pk>[0-9]+)/$', views.editar_contacto_agencia, name="editar_contacto_agencia"),
    #Caso urls
    url(r'^nuevo_caso/(?P<pk_cliente>[0-9]+)/(?P<pk_atiende>[0-9]+)/$', views.nuevo_caso , name="nuevo_caso"),
    url(r'^actualizar_caso/(?P<pk>[0-9]+)/$', views.actualizar_caso, name="actualizar_caso"),
    url(r'^detalle_caso/(?P<pk>[0-9]+)/$', views.detalle_caso, name="detalle_caso"),
    url(r'^solicitar_revision/$', views.solicitar_revision, name="solicitar_revision"),
    url(r'^revision_realizada/$', views.revision_realizada, name="revision_realizada"),
    #Interacciones urls
    url(r'^agregar_interaccion/(?P<pk_caso>[0-9]+)/$', views.agregar_interaccion , name="agregar_interaccion"),
    #Anotaciones urls
    url(r'^agregar_anotacion/(?P<pk_caso>[0-9]+)/$', views.agregar_anotacion , name="agregar_anotacion"),
    #Documentacion urls
    url(r'^nueva_documentacion_caso/(?P<pk_caso>[0-9]+)/$', views.nueva_documentacion_caso, name="nueva_documentacion_caso"),
    url(r'^actualizar_documentacion_caso/(?P<pk>[0-9]+)/$', views.actualizar_documentacion_caso, name="actualizar_documentacion_caso"),
    #pdf
    url(r'^pdf/$', views.get_report , name="PDF"),
]