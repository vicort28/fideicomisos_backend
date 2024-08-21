from rest_framework import serializers, viewsets
from .models import Prestamo, Empleado, PrestamoAprobado , SeguroVida, GastosFunerarios
from rest_framework.exceptions import NotFound

class EmpleadoSerializer(serializers.ModelSerializer):
    
    
    
    nombreCompleto = serializers.CharField(write_only=True, required=False)
    
    
    

    class Meta:
        model = Empleado
        fields = [
            'id', 'numeroEmpleado', 'nombres', 'apellidoPaterno', 'apellidoMaterno', 
            'nombreCompleto', 'rfc', 'curp', 'telefono1', 'telefono2',
            'direccion', 'direccionGeneral', 'correo', 'domicilio', 
            'fechaIngreso', 'fechaNacimiento', 'jubilacionSolicitada' 
        ]

    def create(self, validated_data):
        # Mapear los campos de datos externos a los campos del modelo
       
    
        validated_data['domicilio'] = validated_data.pop('domicilio', '')
        
        validated_data['nombre_completo'] = validated_data.pop('nombreCompleto', '')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Mapear y actualizar los campos
        
       
        instance.unidad = validated_data.pop('direccionGeneral', instance.unidad)
        instance.fecha_nacimiento = validated_data.pop('direccionGeneral', instance.fecha_nacimiento)
        instance.nombre_completo = validated_data.pop('nombreCompleto', instance.nombre_completo)

        # Actualizar cualquier otro campo
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer
    
        

class PrestamoSerializer(serializers.ModelSerializer):
    nombre_empleado = serializers.CharField(source='empleado.nombres', read_only=True)
    apellido_paterno_empleado = serializers.CharField(source='empleado.apellidoPaterno', read_only=True)
    apellido_materno_empleado = serializers.CharField(source='empleado.apellidoMaterno', read_only=True)

    class Meta:
        model = Prestamo
        fields = '__all__' 

class SeguroVidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguroVida
        fields = '__all__' 



class GastosFunerariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = GastosFunerarios
        fields = '__all__' 



class PrestamoAprobadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrestamoAprobado
        fields = ['empleado_id', 'cantidad', 'quincenas', 'estatus', 'pagoporquincena', 'nombre_empleado,', 'apellido_paterno_empleado', 'apellido_materno_empleado']