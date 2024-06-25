

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('agregar-proyecto/', views.agregar_proyecto, name='agregar_proyecto'),
    path('eliminar-proyecto/<int:proyecto_id>/', views.eliminar_proyecto, name='eliminar_proyecto'),
    path('tareas/', views.tareas, name='tareas'),
    path('trabajadores/', views.trabajadores, name='trabajadores'),
    path('tareas_trabajadores/', views.tareas_trabajadores, name='tareas_trabajadores'),
    path('enviar-correo/', views.enviar_correo, name='enviar_correo'),
    path('generar-pdf/', views.generar_pdf, name='generar_pdf'),
]
