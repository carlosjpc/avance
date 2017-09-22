from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

def print_contrato_maestro(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='RightAlign', fontName='Arial', fontSize=10, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='CenterAlign', fontName='Arial', alignment=TA_CENTER))

        elements.append(Paragraph("Contrato No."), styles['RightAlign'])
        elements.append(Paragraph("CONTRATO MAESTRO DE ARRENDAMIENTO DE EQUIPO"), styles['CenterAlign'])
        elements.append(Paragraph("""CONTRATO MAESTRO DE ARRENDAMIENTO DE EQUIPO (EL "CONTRATO DE ARRENDAMIENTO
                                  OPERATIVO Y/O ARRENDAMIENTO MAESTRO") DE FECHA 27 DE ABRIL DE 2017 QUE CELEBRAN
                                  ARRENDADORA AVANCE, SA. DE C.V.  COMO EL "ARRENDADOR", Y LAS PERSONAS FISICAS
                                  Y/O MORALES QUE A CONTINUACION SE SENALAN COMO "ARRENDATARIO", DE ACUERDO CON
                                  LAS SIGUIENTES DECLARACIONES Y CLAUSULAS:"""))


        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
