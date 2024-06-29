

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'), 
    path('tareas/', views.tareas, name='tareas'),
    path('trabajadores/', views.trabajadores, name='trabajadores'),
    path('tareas-trabajadores/', views.tareas_trabajadores, name='tareas_trabajadores'), 
    path('generar-pdf/', views.generar_pdf, name='generar_pdf'),
    path('enviar-correo/', views.enviar_correo, name='enviar_correo'),
]
