# -*- coding: utf-8 -*-
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from datetime import datetime, timedelta
from django.utils.html import conditional_escape as esc
from django.http import HttpResponse

# reportlab imports
from io import BytesIO
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak,
                                TableStyle, Spacer)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

# app imports
from comercial.models import Cita, Interaccion, Caso


def next_weekday(d, weekday):
    days_ahead = int(weekday) - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days=days_ahead)


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
                        body.append('<a data-id='+str(cita.pk) +
                                    ' class="cita">')
                        body.append(esc(cita))
                    elif isinstance(cita, Interaccion):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk) +
                                    ' class="interaccion">Llamar ')
                        body.append(esc(cita.del_Caso.Cliente.Nombre_Empresa))
                    elif isinstance(cita, Caso):
                        body.append('<li class="evento">')
                        body.append('<a data-id='+str(cita.pk) +
                                    ' class="caso">Llamar ')
                        body.append(esc(cita))
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


def comparativaPDF(monto, plazo, ap_adicional, renta_av, deduc_renta_av,
                   pago_ini_av, vr_avance, competencia, pago_inicial,
                   renta, deduccion_mensual, vr, mnod_av, mnod,
                   d_total_av, d_total):
    # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            pdf_name = "comparativa.pdf"
            buff = BytesIO()
            doc = SimpleDocTemplate(buff,
                                    pagesize=landscape(letter),
                                    rightMargin=40,
                                    leftMargin=150,
                                    topMargin=60,
                                    bottomMargin=45,
                                    )
            PAGE_WIDTH = letter[0]

            # Our container for 'Flowable' objects
            elements = []

            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()

            # Set some styles for paragraphs
            styles.add(ParagraphStyle(name='RightAlign',
                                      fontSize=13,
                                      alignment=TA_RIGHT,
                                      ))
            styles.add(ParagraphStyle(name='LeftAlign',
                                      fontSize=13,
                                      alignment=TA_LEFT))
            styles.add(ParagraphStyle(name='Titulo',
                                      fontSize=28,
                                      textColor=colors.red,
                                      alignment=TA_LEFT))
            styles.add(ParagraphStyle(name='Justified',
                                      fontSize=13,
                                      alignment=TA_JUSTIFY))

            # Set some styles for tables
            Cuadricula = TableStyle([('GRID', (0, 0), (-1, -1), 0.25,
                                      colors.blue),
                                     ('BOX', (0, 0), (-1, -1), 0.50,
                                      colors.blue),
                                     ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                                     ('VALIGN', (0, 0), (-1, -1), 'TOP'), ])

            # Start to write document
            elements.append(Paragraph("Comparativa " + competencia +
                                      " / Avance", styles['Titulo']))
            elements.append(Spacer(1, 0.5*inch))
            x = PAGE_WIDTH-(1*inch)
            colwidths = (x/2, x/4, x/4)
            rowheights = (0.3*inch)
            data = ((Paragraph("Factura $" + str(monto) + " | " + str(plazo) +
                               " meses", styles['LeftAlign']),
                     Paragraph(competencia, styles['LeftAlign']),
                     Paragraph("Avance", styles['LeftAlign']),),
                    (Paragraph("Pago Inicial", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(pago_inicial)),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(pago_ini_av)),
                               styles['RightAlign']),),
                    (Paragraph("Renta", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(renta)),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(renta_av)),
                               styles['RightAlign']),),
                    (Paragraph("Deducción Renta", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(deduccion_mensual)),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(deduc_renta_av)),
                               styles['RightAlign']),),
                    (Paragraph("Valor Residual", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(vr)),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(vr_avance)),
                               styles['RightAlign']),),
                    (Paragraph("Monto no Deducible", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(mnod)),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(mnod_av)),
                               styles['RightAlign']),),
                    (Paragraph("Costo Real Monto no Deducible",
                               styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(int(mnod/0.7))),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(int(mnod_av/0.7))),
                               styles['RightAlign']),),
                    (Paragraph("Deducción Total", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(d_total)),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(d_total_av)),
                               styles['RightAlign']),),
                    (Paragraph("Ahorro ISR", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(int(d_total*0.3))),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(
                               int(d_total_av*0.3))),
                               styles['RightAlign']),),
                    (Paragraph("Costo Real", styles['LeftAlign']),
                     Paragraph(" $  " + str("{:,}".format(
                               int(mnod/0.7 + d_total*0.7))),
                               styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(
                               int(mnod_av/0.7 + d_total_av*0.7))),
                               styles['RightAlign']),),
                    (Paragraph("Ahorro Avance", styles['LeftAlign']),
                     Paragraph(" ", styles['RightAlign']),
                     Paragraph(" $  " + str("{:,}".format(int(
                               (mnod/0.7 + d_total*0.7) -
                               (mnod_av/0.7 + d_total_av*0.7)))),
                               styles['RightAlign']),),
                    )
            t = Table(data, colwidths, rowheights, hAlign='LEFT')
            t.setStyle(Cuadricula)
            elements.append(t)
            doc.multiBuild(elements, canvasmaker=PresentacionCanvas)
            response.write(buff.getvalue())
            buff.close()
            return response


class PresentacionCanvas(canvas.Canvas):

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
        direccion = "arrendadoraavance.com.mx"
        p_lateral = '/home/django/django_project/static/lateral_p.jpg'
        logo = '/home/django/django_project/static/avancelogo.jpg'
        self.saveState()
        self.drawImage(p_lateral,  0, 0, width=1.7*inch, height=9*inch,)
        # Footer
        self.setFont('Times-Roman', 10)
        self.setFillColorRGB(0.54, 0.54, 0.54)
        self.drawString(160, 40, direccion)
        self.drawImage(logo,  620, 40, width=1.2*inch,
                       height=0.4*inch)
        self.restoreState()
