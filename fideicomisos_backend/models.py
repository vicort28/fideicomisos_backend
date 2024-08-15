from decimal import Decimal
from django.db import models

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    numeroEmpleado = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=50)
    direccion = models.TextField(max_length=100, default='')
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)
    telefono1 = models.CharField(max_length=15)
    telefono2 = models.CharField(max_length=15, blank=True, null=True) 
    domicilio = models.CharField(max_length=200)
    correo = models.EmailField()
    unidad = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13)
    curp = models.CharField(max_length=18)
    fecha_ingreso = models.DateField(blank=True, null=True) 
    fecha_nacimiento = models.DateField(blank=True, null=True) 
    nombre_completo = models.CharField(max_length=80, default='')

    def __str__(self):
        return f'{self.nombres} {self.apellidoPaterno} {self.apellidoMaterno}'


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

    empleado = models.ForeignKey(Empleado, related_name='prestamo', on_delete=models.CASCADE, null=True)
    cantidad = models.CharField(max_length=10, choices=OPCIONES_CANTIDAD)
    quincenas = models.CharField(max_length=2, choices=OPCIONES_QUINCENAS)
    aprobado = models.BooleanField(default=False)
    estatus = models.CharField(max_length=20, default='pendiente')
    pagoporquincena = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.cantidad and self.quincenas:
            self.pagoporquincena = Decimal(self.cantidad.replace('$', '').replace(',', '')) / Decimal(self.quincenas)
        super(Prestamo, self).save(*args, **kwargs)


class SeguroVida(models.Model):
    empleado = models.ForeignKey(Empleado, related_name='seguros_vida', on_delete=models.CASCADE, null=True)
    # fecha_fallecimiento = models.DateTimeField(blank=False, null=False)
    nombre = models.CharField(max_length=100,  default='')
    apellido_paterno= models.CharField(max_length=100,  default='')
    apellido_materno= models.CharField(max_length=100, default='')
    porcentaje=models.DecimalField(default=0.00, max_digits=5, decimal_places=2, help_text="Ingresa el porcentaje (0.00 - 100.00)")
    padre = models.BooleanField(default=False)
    madre = models.BooleanField(default=False)
    hijo = models.BooleanField(default=False)
    esposo = models.BooleanField(default=False) 


    def __str__(self):
        return f'Seguro de Vida de {self.nombre}'

class GastosFunerarios(models.Model):
    empleado = models.ForeignKey(Empleado, related_name='gastos_funerarios', on_delete=models.CASCADE, null=True)
    padre = models.BooleanField(default=False)
    madre = models.BooleanField(default=False)
    hijo = models.BooleanField(default=False)
    esposo = models.BooleanField(default=False)

    def __str__(self):
        return f"Gastos Funerarios para {self.empleado}"

class PrestamoAprobado(models.Model):
  
    cantidad = models.CharField(max_length=10)
    quincenas = models.IntegerField()
    pago_por_quincena = models.DecimalField(max_digits=10, decimal_places=2, default=0)
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
