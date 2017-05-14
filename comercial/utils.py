from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from datetime import datetime, timedelta
from django.utils.html import conditional_escape as esc

from comercial.models import Cita, Interaccion, Caso

def next_weekday(d, weekday):
    days_ahead = int(weekday) - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days = days_ahead)

class AgendaCalendar(HTMLCalendar):

    def __init__(self, citas):
        super(AgendaCalendar, self).__init__()
        self.citas = self.group_by_day(citas)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.citas:
                cssclass += ' filled'
                body = ['<ul>']
                for cita in self.citas[day]:
                    if isinstance(cita, Cita):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk)+' class="cita">')
                        body.append(esc(cita))
                    elif isinstance(cita, Interaccion):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk)+' class="interaccion">Llamar ')
                        body.append(esc(cita.del_Caso.Cliente.Nombre_Empresa))
                    elif isinstance(cita, Caso):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk)+' class="caso">Llamar ')
                        body.append(esc(cita.Cliente.Nombre_Empresa))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(AgendaCalendar, self).formatmonth(year, month)

    def group_by_day(self, citas):
        field = []
        items = []
        for cita in citas:
            if isinstance(cita, Cita):
                num_dia = cita.Fecha.day
            elif isinstance(cita, Interaccion) or isinstance(cita, Caso):
                num_dia = cita.Buscar_el.day
            if not num_dia in field:
                field.append(num_dia)
                x = field.index(num_dia)
                items.insert(x, [cita])
            else:
                x = field.index(num_dia)
                items[x].append(cita)

        return dict(zip(field, items))

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
