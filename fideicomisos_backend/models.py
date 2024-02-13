from decimal import Decimal
from django.db import models

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    n_empleado = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    domicilio = models.CharField(max_length=200)
    correo = models.EmailField()
    unidad = models.CharField(max_length=100)
    antiguedad = models.PositiveIntegerField()
    rfc = models.CharField(max_length=13)
    curp = models.CharField(max_length=18)

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'


class Prestamo(models.Model):
    OPCIONES_CANTIDAD = [
        ('$5,000.00', '$5,000.00'),
        ('$10,000.00', '$10,000.00'),
        ('$15,000.00', '$15,000.00'),
        ('$20,000.00', '$20,000.00'),
    ]

    OPCIONES_QUINCENAS = [
        ('24', '24'),
        ('48', '48'),
    ]

    empleado = models.ForeignKey(Empleado, related_name='prestamos', on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=10, choices=OPCIONES_CANTIDAD)
    quincenas = models.CharField(max_length=2, choices=OPCIONES_QUINCENAS)
    aprobado = models.BooleanField(default=False)
    estatus = models.CharField(max_length=20, default='pendiente')
    pagoporquincena = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calcula el pago por quincena antes de guardar el objeto
        if self.cantidad and self.quincenas:
            self.pagoporquincena = Decimal(self.cantidad.replace('$', '').replace(',', '')) / Decimal(self.quincenas)
        super(Prestamo, self).save(*args, **kwargs)

class SeguroVida(models.Model):
    empleado = models.ForeignKey(Empleado, related_name='seguros_vida', on_delete=models.CASCADE, null=True)
    fecha_fallecimiento = models.DateTimeField(blank=False, null=False)
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    beneficiario = models.CharField(max_length=100)

    def __str__(self):
        return f'Seguro de Vida de {self.beneficiario}'

class GastosFunerarios(models.Model):
    OPCIONES_PARENTESCO = [
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Esposo', 'Esposo'),
        ('Hijo', 'Hijo'),
    ]

    empleado = models.ForeignKey(Empleado, related_name='gastos_funerarios', on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=10, choices=OPCIONES_PARENTESCO, null=True)

    def __str__(self):
        return f"Gastos Funerarios para {self.empleado.nombre} {self.empleado.apellido_paterno}"
    
class PrestamoAprobado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=10)
    quincenas = models.IntegerField()
    fecha_aprobacion = models.DateField(auto_now_add=True)

    nombre_empleado = models.CharField(max_length=100, blank=True)
    apellido_paterno_empleado = models.CharField(max_length=100, blank=True)
    apellido_materno_empleado = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Prestamo Aprobado para {self.empleado.nombre} {self.empleado.apellido_paterno}"
    
    def save(self, *args, **kwargs):
        self.nombre_empleado = self.empleado.nombre
        self.apellido_paterno_empleado = self.empleado.apellido_paterno
        self.apellido_materno_empleado = self.empleado.apellido_materno
        super().save(*args, **kwargs)