# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from comercial.models import Agencia_Automotriz, Contacto_Agencia

# Create your models here.


class Cuenta_Bancaria(models.Model):
    bbva = 'bv'
    citi = 'cb'
    banorte = 'bn'
    santander = 'st'
    hsbc = 'hs'
    inbursa = 'in'
    ban_regio = 'br'
    ban_bajio = 'bb'
    bank_choices = (
        (bbva, 'BBVA'),
        (citi, 'Citi Banamex'),
        (banorte, 'Banorte'),
        (santander, 'Santander'),
        (hsbc, 'HSBC'),
        (inbursa, 'Inbursa'),
        (ban_regio, 'Ban Regio'),
        (ban_bajio, 'Ban Bajio'),
    )
    Banco = models.CharField(max_length=2, choices=bank_choices, default=bbva)
    Sucursal = models.CharField(max_length=10, blank=True, null=True)
    Num_Cuenta = models.CharField(max_length=10, blank=True, null=True)
    Clave_Interbancaria = models.CharField(max_length=18,
                                           blank=True, null=True)
    Agencia = models.ForeignKey(Agencia_Automotriz, blank=True, null=True)
