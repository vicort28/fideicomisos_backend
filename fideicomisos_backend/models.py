from decimal import Decimal
from django.db import models

class Empleado(models.Model):
    id = models.AutoField(primary_key=True)
    numeroEmpleado = models.CharField(max_length=50, unique=True)
    nombres = models.CharField(max_length=50)
    direccion = models.TextField(max_length=100,blank=True, default='',  null=True)
    apellidoPaterno = models.CharField(max_length=100)
    apellidoMaterno = models.CharField(max_length=100)
    telefono1 = models.CharField(max_length=15, null=True, default='Sin registro', blank=True)
    telefono2 = models.CharField(max_length=15, blank=True, null=True) 
    domicilio = models.CharField(max_length=200, blank=True)
    correo = models.EmailField(blank=True, null=True)
    direccionGeneral = models.CharField(max_length=100, blank=True, null=True)
    rfc = models.CharField(max_length=13, blank=True,  null=True)
    curp = models.CharField(max_length=18, blank=True,  null=True)
    fechaIngreso = models.DateField(blank=True,  null=True) 
    fechaNacimiento = models.DateField(blank=True, null=True) 
    nombre_completo = models.CharField(max_length=80, default='')
    jubilacionSolicitada = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nombres} {self.apellidoPaterno} {self.apellidoMaterno}'


class Prestamo(models.Model):
    OPCIONES_CANTIDAD = [
        ('5,000.00', '5,000.00'),
        ('10,000.00', '10,000.00'),
        ('15,000.00', '15,000.00'),
        ('20,000.00', '20,000.00'),
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
    
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, default='')
    cantidad = models.CharField(max_length=10)
    quincenas = models.IntegerField()
    pago_por_quincena = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_aprobacion = models.DateField(auto_now_add=True)
    nombre_empleado = models.CharField(max_length=100, blank=True)
    apellido_paterno_empleado = models.CharField(max_length=100, blank=True)
    apellido_materno_empleado = models.CharField(max_length=100, blank=True)       
    def __str__(self):
        return f"Prestamo Aprobado para {self.empleado.nombres} {self.empleado.apellidoPaterno}"
    def save(self, *args, **kwargs):
        self.nombre_empleado = self.empleado.nombres
        self.apellido_paterno_empleado = self.empleado.apellidoPaterno
        self.apellido_materno_empleado = self.empleado.apellidoMaterno
        super().save(*args, **kwargs)

