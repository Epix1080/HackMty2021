import pyqrcode
import random
import string
from fpdf import FPDF
import os

def generate_keyword():
    letters = string.ascii_lowercase
    x = ( ''.join(random.choice(letters) for i in range (10)) )
    return x


def qrcode(link):
    name = link
    k = pyqrcode.create(name)
    k.png("codigoqr.png", scale=10)

#PDF
def crear_pdf(string, receta, doctor, paciente):
    qrcode(string)
    pdf = FPDF("P","mm","A4")
    pdf_h = 297
    pdf_w = 210
    pdf.add_page()
    pdf.set_line_width(0.0)
    pdf.line(0,99,210,99)
    pdf.line(0,99*2,210,99*2)
    pdf.image(name = "codigoqr.png", x= 6.0, y= 6.0, w=1586/35, h=1920/40, type= "PNG")
    pdf.set_font('Arial', 'B', 25)
    pdf.set_text_color(220, 50, 50)
    pdf.set_xy(0,0)
    pdf.cell(w = 210.0, h = 25.0, align = 'C', txt = "Información Receta", border = 0)
    pdf.set_xy(0, 99)
    pdf.cell(w = 210.0, h = 25.0, align = 'C', txt = "Información Doctor", border = 0)
    pdf.set_xy(0, 99 * 2)
    pdf.cell(w = 210.0, h = 25.0, align = 'C', txt = "Información Paciente", border = 0)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0,0,0)
    pdf.set_xy(70, 25)
    i = 0
    for j in receta:
        for x in j:
            i += 5
            pdf.set_xy(50, 15 + i)
            pdf.cell(w = 155,h = 7,txt = str(x))

    infoDoctor = ("Nombre: " + doctor[0][2] + "\nEspecialidad: " + doctor[0][3] + \
    "\nHospital de residencia: " + doctor[0][4])
    infoPaciente = ("Nombre: " + paciente[0][2] + "\nFecha de Nacimiento: " + str(paciente[0][3]))
    pdf.set_xy(10, 120)
    pdf.multi_cell(w = 190, h = 7, txt = infoDoctor)
    pdf.set_xy(10, 220)
    pdf.multi_cell(w = 190, h = 7, txt= infoPaciente)
    pdf.output("test.pdf","F")
    os.system("test.pdf")