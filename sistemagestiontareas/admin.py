from django.contrib import admin
from .models import Proyecto, Tarea, Trabajador, TareaTrabajador

admin.site.register(Proyecto)
admin.site.register(Tarea)
admin.site.register(Trabajador)
admin.site.register(TareaTrabajador)
