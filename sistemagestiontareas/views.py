
from django.shortcuts import render
from .models import Proyecto, Tarea, Trabajador, TareaTrabajador

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Proyecto
from .forms import ProyectoForm
from django.core.mail import send_mail
from django.conf import settings
from .models import Trabajador

def home(request):
    proyectos = Proyecto.objects.all()
    form = ProyectoForm()
    return render(request, 'index.html', {'proyectos': proyectos, 'form': form})

def agregar_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, pk=proyecto_id)
    proyecto.delete()
    return JsonResponse({'message': 'Proyecto eliminado correctamente.'})
def tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'tareas.html', {'tareas': tareas})

def trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'trabajadores.html', {'trabajadores': trabajadores})

def tareas_trabajadores(request):
    tareas_trabajadores = TareaTrabajador.objects.all()
    return render(request, 'tareas_trabajadores.html', {'tareas_trabajadores': tareas_trabajadores})

def enviar_correo(request):
    if request.method == 'POST':
        trabajadores = Trabajador.objects.all()
        destinatarios = [trabajador.correo for trabajador in trabajadores]

        asunto = "Hola"
        mensaje = "Hola, aquí te paso los archivos hasta el momento."
        remitente = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(asunto, mensaje, remitente, destinatarios)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False}, status=400)
def generar_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Lista de Proyectos:")
    proyectos = Proyecto.objects.all()
    y = 730
    for proyecto in proyectos:
        p.drawString(100, y, f"Nombre: {proyecto.nombre}, Descripción: {proyecto.descripcion}")
        y -= 20
        if y < 100:
            p.showPage()
            y = 750
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
