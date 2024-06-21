from rest_framework import serializers
from .models import Prestamo, Empleado , SeguroVida, GastosFunerarios, PrestamoAprobado

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__' 
        
class PrestamoSerializer(serializers.ModelSerializer):
    nombre_empleado = serializers.CharField(source='empleado.nombre', read_only=True)
    apellido_paterno_empleado = serializers.CharField(source='empleado.apellido_paterno', read_only=True)
    apellido_materno_empleado = serializers.CharField(source='empleado.apellido_materno', read_only=True)

    class Meta:
        model = Prestamo
        fields = ['id', 'cantidad', 'quincenas', 'nombre_empleado', 'apellido_paterno_empleado', 'apellido_materno_empleado', 'aprobado']


class SeguroVidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguroVida
        fields = '__all__' 



class GastosFunerariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastosFunerarios
        fields = ['empleado_id', 'madre', 'padre', 'esposo', 'hijo']




class PrestamoAprobadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestamoAprobado
        fields = ['empleado_id', 'cantidad', 'quincenas', 'estatus', 'pagoporquincena', 'nombre_empleado,', 'apellido_paterno_empleado', 'apellido_materno_empleado']