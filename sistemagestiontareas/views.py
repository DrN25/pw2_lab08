

from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from .models import Proyecto, Tarea, Trabajador, TareaTrabajador
from io import BytesIO
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
def home(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'index.html', {'proyectos': proyectos})

def tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas.html', {'tareas': tareas})

def trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'trabajadores.html', {'trabajadores': trabajadores})

def tareas_trabajadores(request):
    tareas_trabajadores = TareaTrabajador.objects.all()
    return render(request, 'tareas_trabajadores.html', {'tareas_trabajadores': tareas_trabajadores})

def generar_pdf(request):
    proyectos = Proyecto.objects.all()
    tareas = Tarea.objects.all()
    trabajadores = Trabajador.objects.all()
    tareas_trabajadores = TareaTrabajador.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="informe_proyectos_tareas.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    elements = []

    elements.append(Paragraph("Informe de Proyectos, Tareas y Trabajadores"))

    elements.append(Paragraph("Proyectos:"))
    proyecto_data = [['ID', 'Nombre', 'Descripción']]
    for proyecto in proyectos:
        proyecto_data.append([str(proyecto.id), proyecto.nombre, proyecto.descripcion])

    proyecto_table = Table(proyecto_data, colWidths=[50, 200, 300])
    proyecto_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ]))
    elements.append(proyecto_table)

    elements.append(Paragraph("<br/><br/>"))

    elements.append(Paragraph("Tareas:"))
    tarea_data = [['ID', 'Nombre', 'Descripción']]
    for tarea in tareas:
        tarea_data.append([str(tarea.id), tarea.nombre, tarea.descripcion])

    tarea_table = Table(tarea_data, colWidths=[50, 200, 300])
    tarea_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ]))
    elements.append(tarea_table)

    elements.append(Paragraph("<br/><br/>"))

    elements.append(Paragraph("Trabajadores:"))
    trabajador_data = [['ID', 'Nombre', 'Correo']]
    for trabajador in trabajadores:
        trabajador_data.append([str(trabajador.id), trabajador.nombre, trabajador.correo])

    trabajador_table = Table(trabajador_data, colWidths=[50, 200, 200])
    trabajador_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ]))
    elements.append(trabajador_table)

    elements.append(Paragraph("<br/><br/>"))

    elements.append(Paragraph("Tareas de Trabajadores:"))
    tt_data = [['Tarea', 'Trabajador']]
    for tt in tareas_trabajadores:
        tt_data.append([tt.tarea.nombre, tt.trabajador.nombre])

    tt_table = Table(tt_data, colWidths=[200, 200])
    tt_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
    ]))
    elements.append(tt_table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def enviar_correo(request):
    try:
        trabajadores = Trabajador.objects.all()
        for trabajador in trabajadores:
            send_mail(
                'Mensaje del Grupo 3 de PWEB2',
                'Hola, este es un mensaje del Grupo 3 de PWEB2.',
                'grupopweb2sh@gmail.com',
                [trabajador.correo],
                fail_silently=False,
            )
        messages.success(request, 'Correos enviados exitosamente.')
    except Exception as e:
        messages.error(request, f'Hubo un error al enviar los correos: {e}')
    return redirect('index')