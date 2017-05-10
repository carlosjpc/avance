from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from datetime import datetime, timedelta
from django.utils.html import conditional_escape as esc

from comercial.models import Cita, Interaccion

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
                    if isinstance(cita,Cita):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk)+' class="cita">')
                        body.append(esc(cita))
                    elif isinstance(cita,Interaccion):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk)+' class="interaccion">Llamar ')
                        body.append(esc(cita.del_Caso.Cliente.Nombre_Empresa))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(AgendaCalendar, self).formatmonth(year, month)

    def group_by_day(self, citas):
        field = lambda citas: citas.Fecha.day
        return dict(
            [(day, list(items)) for day, items in groupby(citas, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
