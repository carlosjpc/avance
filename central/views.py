from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.db.models import Q
from datetime import datetime, timedelta

#internal imports



# Create your views here.

@login_required
def nuevo_usuario(request, tipo):
    if request.method == "POST":
        userform = UserForm(request.POST, instance=User())
        if userform.is_valid():
            new_user = User.objects.create_user(**designerform.cleaned_data)
            if tipo == "vendedor":
                g = Group.objects.get(name='comercial_vendedor')
                g.user_set.add(new_user)
            elif tipo == "vendedor_backup":
                g = Group.objects.get(name='comercial_backup')
                g.user_set.add(new_user)
            else:
                return HttpResponse('<h1>Upps! algo salió mal</h1>')
            url = reverse('user_detail', kwargs={'pk': new_user.pk})
            return HttpResponseRedirect(url)
    userform = UserForm()
    return render(request, 'central/create_user.html', {'userform': userform,})
