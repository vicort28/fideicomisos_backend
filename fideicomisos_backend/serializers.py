from rest_framework import serializers
from .models import Prestamo, Empleado , SeguroVida, GastosFunerarios, PrestamoAprobado

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__' 
        
class PrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamo
        fields = ['empleado_id', 'cantidad', 'quincenas', 'estatus', 'pagoporquincena']

class SeguroVidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguroVida
        fields = ['empleado_id', 'fecha_fallecimiento', 'domicilio', 'telefono', 'beneficiario']

class GastosFunerariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastosFunerarios
        fields = ['empleado_id', 'parentesco']



class PrestamoAprobadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestamoAprobado
        fields = '__all__'  