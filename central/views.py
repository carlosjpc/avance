# -*- coding: utf-8 -*-
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

import os.path

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
from reportlab.pdfgen.canvas import Canvas

# internal imports
from central.models import (Contrato, Anexo, Modificatorio, Factura,
                            Poliza_Seguro, Documentacion_PMoral)
from comercial.models import Cliente

# User checks


def legal_check(user):
    if user:
        return user.groups.filter(name='Legal').count() == 1
    return False

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
    return render(request, 'central/create_user.html',
                  {'userform': userform, })


@login_required
# user_passes_test(legal_check)
def contrato_maestro_pmoral_pdf(request):
    # Get the information for the contract
    cliente = Cliente.objects.get(pk=3)
    # documentacion = Documentacion_PMoral.objects.get(pk=pk_docu)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=45,
                            )
    PAGE_HEIGHT = letter[1]
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
    Cuadricula = TableStyle([('GRID', (0, 0), (-1, -1), 0.25, colors.blue),
                             ('BOX', (0, 0), (-1, -1), 0.50, colors.blue),
                             ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                             ('VALIGN', (0, 0), (-1, -1), 'TOP'), ])

    # Start to write document
    elements.append(Paragraph("Contrato No. 349", styles['RightAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("CONTRATO MAESTRO DE ARRENDAMIENTO DE EQUIPO",
                              styles['CenterAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""CONTRATO MAESTRO DE ARRENDAMIENTO DE EQUIPO (EL "CONTRATO DE ARRENDAMIENTO
                                OPERATIVO Y/O ARRENDAMIENTO MAESTRO") DE FECHA 27 DE ABRIL DE 2017 QUE
                                CELEBRAN ARRENDADORA AVANCE, SA. DE C.V.  COMO EL "ARRENDADOR", Y LAS PERSONAS
                                FISICAS Y/O MORALES QUE A CONTINUACION SE SENALAN COMO "ARRENDATARIO", DE
                                ACUERDO CON LAS SIGUIENTES DECLARACIONES Y CLAUSULAS:""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("P R O E M I O:", styles['CenterAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("A) EL ARRENDATARIO", styles['LeftAlign']))
    elements.append(Spacer(1, 0.3*inch))

    colwidths = (PAGE_WIDTH-(3.3*inch), 2*inch)
    rowheights = (0.3*inch)
    data = ((cliente.Nombre_Empresa, "RFC: " + cliente.RFC), )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    colwidths = (PAGE_WIDTH-(1.3*inch), )
    data = (("Escritura constitutiva de EL ARRENDATARIO:",),)
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    x = PAGE_WIDTH-(1.3*inch)
    colwidths = (x/6, x/6, x/6, x/6, x/3)
    rowheights = (0.8*inch)
    data = ((Paragraph("Escritura Constitutiva No.99,286",
                       styles['LeftAlign']),
             Paragraph("""Ante el Licenciado: Luis Felipe del Valle
                        Prieto Ortega""", styles['LeftAlign']),
             Paragraph("Notario Público No. 20 de la Ciudad de México",
                       styles['LeftAlign']),
             Paragraph("Escritura de fecha: 10 de Febrero de 1992",
                       styles['LeftAlign']),
             Paragraph("""Inscrita en el Registro Público de Comercio (RPPC) de:
                        Tlalnepantla, Estado de México""",
                       styles['LeftAlign']),),
            )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    colwidths = (x/3, x*2/3)
    rowheights = (0.4*inch)
    data = ((Paragraph("Fecha de Inscripción en el RPPC: 26 de Junio de 1992",
             styles['LeftAlign']),
             Paragraph("""Datos de Registro: Partida 359, Volúmen 23,
              Libro Primero de Comercio""",
             styles['LeftAlign']),),
            )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    colwidths = (x/6, x*5/6)
    data = ((Paragraph("Poder de su representante:", styles['LeftAlign']),
             Paragraph("NOMBRE DEL REPRESENTANTE LEGAL:  René Ramiro Pacheco Ortiz", styles['LeftAlign']),),
             )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    colwidths = (x/6, x/6, x/6, x/6, x/3)
    rowheights = (0.8*inch)
    data =  ((Paragraph("Escritura Constitutiva No.99,286", styles['LeftAlign']),
              Paragraph("Ante el Licenciado: Luis Felipe del Valle Prieto Ortega", styles['LeftAlign']),
              Paragraph("Notario Público No. 20 de la Ciudad de México", styles['LeftAlign']),
              Paragraph("Escritura de fecha: 10 de Febrero de 1992", styles['LeftAlign']),
              Paragraph("Inscrita en el Registro Público de Comercio (RPPC) de: Tlalnepantla, Estado de México", styles['LeftAlign']),),
             )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    colwidths = (x/3, x*2/3)
    rowheights = (0.4*inch)
    paragraphs = []
    info3 = Paragraph("Datos de Registro:", styles['LeftAlign'])
    info4 = Paragraph("Partida 359, Volúmen 23, Libro Primero de Comercio", styles['LeftAlign'])
    paragraphs.append(info3)
    paragraphs.append(info4)
    data = ((Paragraph("Fecha de Inscripción en el RPPC: 26 de Junio de 1992",
              styles['LeftAlign']),
              paragraphs,),
             )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    colwidths = (PAGE_WIDTH-( 1.3*inch ),)
    rowheights = (0.3*inch)
    data = (("Domicilio: Avenida de los Frailes 10, Colonia San Andrés Atenco Ampliación, Municipio Tlalnepantla de Baz, C.P. 54040, Estado de México",),)
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("B) EL OBLIGADO SOLIDARIO", styles['LeftAlign']))
    elements.append(Spacer(1, 0.3*inch))
    colwidths = (x/2, x/2)
    rowheights = (0.28*inch)
    data = ((Paragraph("Nombre: René Ramiro Pacheco Ortiz",
                       styles['LeftAlign']),
             Paragraph("Nacionalidad: Mexicana", styles['LeftAlign'])),
            (Paragraph("Originario de: Guanajuato", styles['LeftAlign']),
             Paragraph("Fecha de Nacimiento: 06 de Enero de 1950",
                       styles['LeftAlign'])),
            (Paragraph("Tipo de ID: IFE: 0877008103318", styles['LeftAlign']),
             Paragraph("Caducidad de la ID: 2021", styles['LeftAlign'])),
            )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    rowheights = (0.7*inch)
    data = ((Paragraph("RFC: PAOR500106V63", styles['LeftAlign']),
             Paragraph("""Domicilio: Puerta de Hierro 21, Fraccionamiento
                       Campestre del Lago, Municipio Cuautitlán Izcalli, C.P.
                       54766, Estado de México""", styles['LeftAlign'])),
            )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("C) EL DEPOSITARIO:", styles['LeftAlign']))
    elements.append(Spacer(1, 0.3*inch))
    colwidths = (x/2, x/2)
    rowheights = (0.28*inch)
    data = ((Paragraph("Nombre: René Ramiro Pacheco Ortiz",
                       styles['LeftAlign']),
             Paragraph("Nacionalidad: Mexicana", styles['LeftAlign'])),
            (Paragraph("Originario de: Guanajuato", styles['LeftAlign']),
             Paragraph("Fecha de Nacimiento: 06 de Enero de 1950",
                       styles['LeftAlign'])),
            (Paragraph("Tipo de ID: IFE: 0877008103318", styles['LeftAlign']),
             Paragraph("Caducidad de la ID: 2021", styles['LeftAlign'])),
            )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    rowheights = (0.7*inch)
    data = ((Paragraph("RFC: PAOR500106V63", styles['LeftAlign']),
             Paragraph("""Domicilio: Puerta de Hierro 21, Fraccionamiento
                        Campestre del Lago, Municipio Cuautitlán Izcalli, C.P.
                        54766, Estado de México""", styles['LeftAlign'])),
            )
    t = Table(data, colwidths, rowheights, hAlign='LEFT')
    t.setStyle(Cuadricula)
    elements.append(t)
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("DECLARACIONES", styles['CenterAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("I. El Arrendador declara, representa y garantiza que:", styles['LeftAlign']))
    elements.append(Paragraph("""(a) Es una sociedad anónima de capital variable debidamente constituida de conformidad
                                 con  las leyes de los Estados Unidos Mexicanos (“México”), según consta en la escritura
                                 pública Número 102,858 de fecha 07 de junio de 2004, otorgada ante la fe del Licenciado
                                 Cecilio González Márquez, Titular de la Notaria Pública Número 151 de la Ciudad de México,
                                 debidamente inscrita el Registro Público de la Propiedad y del Comercio de la Ciudad de
                                 México, con fecha 19 de agosto de 2004, bajo el Folio Mercantil Número 323641."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(b) Su objeto social es la compra, venta y arrendamiento de toda clase de bienes
                                 muebles y la prestación de servicios relacionados con los mismos, y por tanto,
                                 está autorizada a celebrar este Contrato de Arrendamiento Operativo."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(c) Sujeto a la suscripción del Anexo de Arrendamiento (según dicho término se define
                                 más adelante) que corresponda, está dispuesto a adquirir del proveedor, distribuidor,
                                 vendedor, fabricante o constructor que le indique el Arrendatario, el Equipo (según
                                 dicho término se define más adelante) descrito en los Anexos de Arrendamiento del
                                 presente, con el propósito de dar en arrendamiento dicho Equipo al Arrendatario,
                                 de conformidad a los términos y condiciones establecidos en el presente Contrato de
                                 Arrendamiento Operativo y los Anexos de Arrendamiento.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(d) Su representante cuenta con el poder y la capacidad necesaria para celebrar
                                 este Arrendamiento Maestro, según consta en la escritura Número 191,574 de fecha
                                 19 de agosto de 2016, otorgada ante la fe del Licenciado Cecilio González Márquez,
                                 Titular de la Notaria Pública Número 151 de la Ciudad de México.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(e) Que su domicilio es el ubicado en: Cracovia 72 BIS, PO18,  Nivel 3, Torre B,
                                 Col. San Ángel, Álvaro Obregón,  Ciudad de México, C.P. 01000""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""II. El Arrendatario  declara, representa y garantiza que:""", styles['LeftAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(a) Cuenta con todas las facultades necesarias para celebrar el presente
                                 Contrato de acuerdo a sus términos y condiciones.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(b) Se encuentra al corriente en el pago de todos los impuestos, derechos,
                                 contribuciones y demás obligaciones a su cargo, así como en los convenios
                                 de los cuales forma parte; """, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(c) Es su deseo tomar en arrendamiento del Arrendador el Equipo descrito
                                 en los Anexos de Arrendamiento del presente, de conformidad con los términos
                                 y condiciones establecidos en el presente Contrato de Arrendamiento Operativo
                                 y los Anexos de Arrendamiento.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(d) Ha seleccionado el Equipo basado en su propio juicio y expresamente niega
                                 haberse basado en declaraciones hechas por el Arrendador.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(e)  Declara que no participa en huelgas, no está en concurso mercantil o
                                 procedimientos similares que pudieran afectar su condición financiera."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(f)  Declara que desde la fecha de la presentación de los estados financieros,
                                 estados de cuenta y/o declaraciones de impuestos (según le corresponda), cuya
                                 copia ha sido entregada a el Arrendador, a la fecha de la firma de este
                                 Contrato y del Anexo de Arrendamiento que Corresponda, no ha ocurrido cambio
                                 alguno que afecte en forma adversa en su situación financiera.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(g) En su caso, ser persona moral constituida de conformidad a las leyes de
                                 México según consta en el instrumento público descrito en el proemio del
                                 presente contrato, así mismo manifiesta que  su representante Legal cuenta
                                 con el poder y la capacidad necesaria para celebrar este Contrato de Arrendamiento
                                 Operativo así como cualquiera de sus Anexos de Arrendamiento, y  que las facultades
                                 que le fueron conferidas no le han sido de ninguna forma revocadas o limitadas."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(h) En términos de la Ley Federal de Protección de Datos Personales en Posesión
                                 de los Particulares y su Reglamento, el Arrendatario declara o en caso de ser
                                 persona moral su(s) apoderado(s) legal(es) declara(n) que ha(n) tenido a su
                                 disposición el aviso de privacidad del Arrendador y su respectivo contenido,
                                 el cual se le(s) ha dado a conocer previamente a la celebración del presente
                                 Contrato de Arrendamiento Operativo y que se encuentra para su consulta en la
                                 página web http://www.arrendadoraavance.com.mx/cotizador/aviso_privacidad.pdf/ ,
                                 por lo que en este acto otorga(n) su consentimiento al Arrendador para el
                                 tratamiento de sus datos personales en términos de dicho aviso de privacidad.
                                 De igual manera reconoce(n) que podrá(n) verificar en dicha página, cualquier
                                 cambio en el mencionado aviso de privacidad.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""III. El Obligado Solidario y/o el Fiador declara, representa y garantiza que:"""
                                 , styles['LeftAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(a) Cuenta con todas las facultades necesarias para celebrar el presente
                                 Contrato de acuerdo a sus términos y condiciones; """, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(b) Se encuentra al corriente en el pago de todos los impuestos, derechos,
                                 contribuciones y demás obligaciones a su cargo, así como en los convenios
                                 de los cuales forma parte;""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(c) Es su deseo obligarse solidariamente y garantizar todas las obligaciones
                                 del Arrendatario en el presente Arrendamiento Maestro y sus Anexos de
                                 Arrendamiento.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(d) El Fiador garantiza el cumplimiento de las obligaciones contraídas
                                 respecto del  presente Arrendamiento Maestro a cargo del Arrendatario,
                                 y las que a la fecha de firma del mismo y en el futuro se puedan derivar
                                 de la firma de sus respectivos Anexos de Arrendamiento, por lo que el
                                 Fiador renunciando expresamente a los beneficios de división orden y
                                 exclusión y a lo dispuesto en el artículo 1851 y 2487 del Código Civil
                                 o a establecer requisitos o condiciones a el Arrendador para que este
                                 pueda reclamar el cumplimiento de pago de las obligaciones contraídas
                                 bajo el Arrendamiento.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(e) Cuenta con los recursos económicos suficientes para dar cumplimiento
                                 a todas y cada una de las obligaciones, en especial las de pago, que
                                 derivan del presente Arrendamiento Maestro a cargo del Arrendatario, y
                                 las que a la fecha de firma del mismo y en el futuro se puedan derivar
                                 de la firma de sus respectivos Anexos de Arrendamiento.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(f) Declara que no participa en huelgas, no está en concurso mercantil
                                 o procedimientos similares que pudieran afectar su condición financiera."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(g) Declara que desde la fecha de presentación de los estados financieros,
                                 estados de cuenta y/o declaraciones de impuestos (según le corresponda),
                                 cuya copia ha sido entregada a el Arrendador, a la fecha de la firma de
                                 este Contrato y del Anexo de Arrendamiento que Corresponda, no ha ocurrido
                                 cambio alguno que afecte en forma adversa en su situación financiera."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(h) En su caso, ser persona moral constituida de conformidad a las leyes de
                                 México según consta en el instrumento público descrito en el proemio del
                                 presente contrato, así mismo manifiesta que  su representante legal cuenta
                                 con el poder y la capacidad necesaria para celebrar este Contrato de
                                 Arrendamiento Operativo así como cualquiera de sus Anexos de Arrendamiento,
                                 y  que las facultades que le fueron conferidas no le han sido de ninguna
                                 forma revocadas o limitadas.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""(i) En términos de la Ley Federal de Protección de Datos Personales en
                                 Posesión de los Particulares y su Reglamento, declaran o en caso de ser
                                 persona moral su(s) apoderado(s) legal(es) declara(n) que ha(n) tenido a
                                 su disposición el aviso de privacidad del Arrendador y su respectivo
                                 contenido, el cual se le ha dado a conocer previamente a la celebración
                                 del presente Contrato de Arrendamiento Operativo y que se encuentra para
                                 su consulta en la página web
                                 http://www.arrendadoraavance.com.mx/cotizador/aviso_privacidad.pdf/ ,
                                 por lo que en este acto otorga(n) su consentimiento al Arrendador para
                                 el tratamiento de sus datos personales en términos de dicho aviso de
                                 privacidad. De igual manera reconoce(n) que podrá(n) verificar en dicha
                                 página, cualquier cambio en el mencionado aviso de privacidad.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""IV. El “DEPOSITARIO” declara, representa y garantiza que:""", styles['LeftAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""a) Cuenta con la capacidad necesaria para celebrar este Contrato de
                                 Arrendamiento Operativo y obligarse en sus términos.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""b) Protesta su legal y fiel desempeño a título gratuito, renunciando expresamente
                                 a percibir cualquier retribución al desempeño de su cargo, así como cualquier
                                 reembolso de gastos que por el desempeño de su cargo tenga que desembolsar,
                                 haciéndose sabedor de las responsabilidades civiles y penales en que incurren
                                 los depositarios sobre todo si se dispusieran de cualquiera de los bienes que
                                 recibe en su carácter de depositario.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""c) Es su deseo constituirse como depositario del Equipo objeto del presente
                                 contrato.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""d) En términos del presente Contrato de Arrendamiento Operativo el “DEPOSITARIO”
                                 se compromete y obliga frente a  “El Arrendador” a hacerle entrega del Equipo
                                 en caso de presentarse un incumplimiento de “El Arrendatario” y siempre y
                                 cuando medie un requerimiento por escrito de “El Arrendador”  por lo que el
                                 “DEPOSITARIO” reconoce y acepta todas las obligaciones y responsabilidades
                                 civiles y penales que la legislación mexicana le establece en su calidad de
                                 “DEPOSITARIO”.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""e) En términos de la Ley Federal de Protección de Datos Personales en
                                 Posesión de los Particulares y su Reglamento, declara que ha tenido a
                                 su disposición el aviso de privacidad del Arrendador y su respectivo
                                 contenido, el cual se le ha dado a conocer previamente a la celebración
                                 del presente Contrato de Arrendamiento Operativo y que se encuentra para
                                 su consulta en la página web
                                 http://www.arrendadoraavance.com.mx/cotizador/aviso_privacidad.pdf , por lo
                                 que en este acto otorga su consentimiento al Arrendador para el tratamiento
                                 de sus datos personales en términos de dicho aviso de privacidad. De igual
                                 manera reconoce que podrá verificar en dicha página, cualquier cambio en
                                 el mencionado aviso de privacidad.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""Conformes las partes con las Declaraciones que anteceden, convienen en las
                                 siguientes:""", styles['LeftAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""CLAUSULAS""", styles['CenterAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""PRIMERA. DEFINICIONES""", styles['LeftAlign']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""Salvo que el contexto de una frase lo requiera de otra forma, los términos
                                 que a continuación se mencionan y que sean escritos con inicial mayúscula a
                                 lo largo del presente Contrato de Arrendamiento Operativo y los Anexos de
                                 Arrendamiento, tendrán los siguientes significados, independientemente que
                                 se utilicen en singular o plural, y las palabras en género masculino se
                                 entenderán en género femenino y viceversa:""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(""""Anexo de Arrendamiento" significará, cada uno de los documentos
                                 (en forma substancialmente igual a lo contenido en el anexo “A” del
                                 presente) que las partes suscriban en uno o sucesivos actos durante
                                 la vigencia del presente Contrato de Arrendamiento Maestro operativo
                                 y que contendrá la descripción del Equipo, así como todas las características
                                 del mismo, incluyendo el Certificado de Aceptación (según se define en
                                 el Arrendamiento Maestro) en la inteligencia de que cada Anexo de Arrendamiento
                                 se numerará progresivamente en forma sucesiva y se sujetará a los términos
                                 y condiciones en el presente Contrato de Arrendamiento Operativo."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Código Civil Aplicable”, significará el Código Civil para el Distrito
                                 Federal.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Código Procesal Aplicable”, significará el Código de Procedimientos
                                 Civiles para el Distrito Federal """, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Contrato de Arrendamiento Operativo” y/o “Arrendamiento Maestro,
                                 es el contrato atípico e innominado por virtud del cual una persona
                                 moral especializada llamada arrendador otorga el uso y goce temporal
                                 de un bien mueble por plazo determinado y forzoso, a una persona física
                                 o moral llamada arrendatario la cual se obliga a pagar una contraprestación
                                 en dinero o en especie llamada renta. """, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Día Hábil”, significará cualquier día en el cual los bancos estén abiertos
                                 para realizar operaciones bancarias ordinarias en la Ciudad de México, México
                                 y en la Ciudad de Nueva York, Nueva York, Estados Unidos de América."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Equipo”, significará el o los bienes y, en general conjuntamente, todos
                                 los activos que se describan en cada uno de los Anexos de Arrendamiento,
                                 y que son arrendados conforme a dicho Anexo de Arrendamiento y al presente,
                                 incluyendo todos los repuestos, partes, reparaciones, adiciones, agregados
                                 y accesorios que sean incorporados al mismo, ya sea que hayan sido hechos
                                 por el Arrendador o por el Arrendatario. Cualquier referencia u obligación
                                 respecto al Equipo se entenderá en todos los casos como un todo,
                                 independientemente del o los bienes y el o los activos descritos en el
                                 Anexo de Arrendamiento que corresponda.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Fecha de Inicio” significará la fecha en que el Plazo Básico Forzoso
                                 de un Anexo de Arrendamiento comience, en la inteligencia de que dicha
                                 fecha será la que se establezca en el Anexo de Arrendamiento respectivo."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“IVA”, significará el Impuesto al Valor Agregado.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Pagos Periódicos”, significará los pagos parciales y consecutivos, que para
                                 efecto de conveniencia, el Arrendatario efectuará por concepto de la Renta,
                                 durante los periodos convenidos por las partes en los términos del Anexo de
                                 Arrendamiento que corresponda. """, styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Plazo Básico Forzoso”, significará el plazo durante el cual cualquier Anexo
                                 de Arrendamiento del presente Contrato de Arrendamiento Operativo estará en
                                 vigor, el cual comenzará en la Fecha de Inicio.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Reducciones”, significará cualquier retención, reducción, compensación,
                                 defensa, contrademanda o reconvención, no importa cómo se designe o la
                                 razón de la misma.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Renta”, significará la cantidad total que el Arrendatario deberá pagar
                                 al Arrendador por el arrendamiento del Equipo, tal y como se convenga en
                                 cada Anexo de Arrendamiento de Equipo, más el IVA en vigor."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Software” tiene el significado atribuido a dicho término en la Cláusula
                                 Vigésima de este Contrato de Arrendamiento Operativo.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""“Administración de arrendamiento” significará el pago distinto a las Rentas
                                 de los equipos y que el Arrendatario se obliga a pagar al Arrendador,
                                 incluyendo sin que sea limitativo, gastos de mantenimiento,  alta y baja de
                                 placas,  seguros, impuestos mismo que deberá ser cubierto a más tardar a
                                 los 5 (cinco) días naturales a partir de la solicitud del Arrendador."""
                                 , styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""Todas las cantidades a que se haga referencia en este Contrato de
                                 Arrendamiento Operativo y cualquier Anexo de Arrendamiento serán en pesos,
                                 moneda de curso legal de los Estados Unidos Mexicanos.""", styles['Justified']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("""""", styles['Justified']))

    doc.multiBuild(elements, canvasmaker=ContratoCanvas)
    response.write(buff.getvalue())
    buff.close()
    return response


class ContratoCanvas(canvas.Canvas):

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
        self.drawImage(logo,  45, letter[1] - 50, width=1.2*inch,
                       height=0.4*inch)
        self.setStrokeColorRGB(0.54, 0.54, 0.54)
        self.setLineWidth(0.2)
        # Linea de arriba
        self.line(40, letter[1] - 57, letter[0] - 40, letter[1] - 57)
        # Linea de abajo
        self.line(40, 55, letter[0] - 40, 55)
        # Linea derecha
        self.line(40, 55, 40, letter[1] - 57)
        # Linea izquierda
        self.line(letter[0] - 40, 55, letter[0] - 40, letter[1] - 57)
        # Footer
        self.setFont('Times-Roman', 10)
        self.setFillColorRGB(0.54, 0.54, 0.54)
        self.drawString(letter[0]/2 - 40, 40, page)
        self.drawString(42, 30, direccion1)
        self.drawString(42, 20, direccion2)
        self.drawString(42, 10, direccion3)
        self.restoreState()
