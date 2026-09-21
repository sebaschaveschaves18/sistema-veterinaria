from django.db import models


class Propietario(models.Model):
    identificacion = models.CharField(max_length=30)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2)
    activo = models.BooleanField(default=True)
    propietario = models.ForeignKey(
        Propietario,
        on_delete=models.CASCADE,
        related_name='mascotas'
    )

    def __str__(self):
        return self.nombre


class ConsultaVeterinaria(models.Model):
    mascota = models.ForeignKey(
        Mascota,
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    fecha = models.DateField(auto_now_add=True)
    motivo = models.CharField(max_length=200)
    diagnostico = models.CharField(max_length=300)
    tratamiento = models.CharField(max_length=300)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.mascota.nombre} - {self.fecha}'
