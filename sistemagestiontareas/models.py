from django.db import models

class Proyecto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    proyecto = models.ForeignKey(Proyecto, related_name='tareas', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')])

    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class TareaTrabajador(models.Model):
    tarea = models.ForeignKey(Tarea, related_name='trabajadores', on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, related_name='tareas_asignadas', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tarea', 'trabajador')

    def __str__(self):
        return f'Tarea: {self.tarea.nombre} - Trabajador: {self.trabajador.nombre}'
