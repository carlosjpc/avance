# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm

from admon.models import Cuenta_Bancaria


class Cuenta_BancariaForm(ModelForm):
    class Meta:
        model = Cuenta_Bancaria
        fields = ('Banco', 'Sucursal', 'Num_Cuenta', 'Clave_Interbancaria')
