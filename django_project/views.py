from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required


@login_required
def login_redirect(request):
    user = request.user
    if user.groups.filter(name='comercial_vendedor').count() == 1:
        return HttpResponseRedirect("/comercial/ctrl_panel_vendedor/")
    elif user.groups.filter(name='comercial_backup').count() == 1 or user.groups.filter(name='comercial_mger').count() == 1:
        return HttpResponseRedirect("/comercial/ctrl_panel_backup/")
