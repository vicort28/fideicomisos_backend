from collections import Counter
import traceback
from django.http import JsonResponse
from .models import Prestamo, PrestamoAprobado, SeguroVida, GastosFunerarios
from .models import Empleado
from rest_framework.decorators import api_view
from .serializers import PrestamoAprobadoSerializer, PrestamoSerializer, EmpleadoSerializer, SeguroVidaSerializer, GastosFunerariosSerializer
from django.views.decorators.csrf import csrf_exempt
import json 
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.db.models import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404



# Django view
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prestamo, Empleado
from .serializers import PrestamoSerializer

# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prestamo, Empleado
from .serializers import PrestamoSerializer

@api_view(['POST'])
@csrf_exempt
def guardar_formulario(request):
    if request.method == 'POST':
        datos_formulario1 = request.data
        empleado_id = datos_formulario1.get('empleado_id')

        try:
            empleado = Empleado.objects.get(pk=empleado_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Empleado no encontrado o ID de empleado no válido'}, status=400)

        serializer = PrestamoSerializer(data=datos_formulario1)

        if serializer.is_valid():
            # Guarda el préstamo y obtén el objeto creado
            prestamo = serializer.save(empleado=empleado)
            
            # Calcula el pago por quincena y actualiza el objeto
            cantidad = float(prestamo.cantidad.replace('$', '').replace(',', ''))
            quincenas = float(prestamo.quincenas)
            prestamo.pagoporquincena = cantidad / quincenas
            prestamo.save()

            return JsonResponse({'mensaje': 'Datos del formulario guardados correctamente'}, status=201)
        else:
            return JsonResponse({'error': 'Datos del formulario no válidos', 'detalles': serializer.errors}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@api_view(['POST'])
def guardar_seguro_vida(request):
    if request.method == 'POST':
        datos_seguro_vida = request.data
        serializer = SeguroVidaSerializer(data=datos_seguro_vida)

        if serializer.is_valid():
            empleado_id = datos_seguro_vida.get('empleado_id')
            
            try:
                empleado = Empleado.objects.get(pk=empleado_id)
            except Empleado.DoesNotExist:
                return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(empleado=empleado)
            return Response({'mensaje': 'Seguro de vida registrado correctamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Datos del seguro de vida no válidos'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@api_view(['POST'])
def guardar_gastos_funerarios(request):
    if request.method == 'POST':
        datos_gastos_funerarios = request.data
        empleado_id = datos_gastos_funerarios.get('empleado_id')

        try:
            empleado = Empleado.objects.get(pk=empleado_id)
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GastosFunerariosSerializer(data=datos_gastos_funerarios)

        if serializer.is_valid():
            serializer.validated_data['parentesco'] = serializer.validated_data.get('parentesco', 'padre')

            gastos_funerarios = serializer.save(empleado=empleado)
            return Response({'mensaje': 'Datos de gastos funerarios registrados correctamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Datos de gastos funerarios no válidos', 'detalles': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




@csrf_exempt
def agregar_empleado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            nuevo_empleado = Empleado(
                nombre=data.get('nombre', ''),
                apellido_paterno=data.get('apellido_paterno', ''),
                apellido_materno=data.get('apellido_materno', ''),
                telefono=data.get('telefono', ''),
                domicilio=data.get('domicilio', ''),
                correo=data.get('correo', ''),
                unidad=data.get('unidad', ''),
                antiguedad=data.get('antiguedad', 0),
                rfc=data.get('rfc', ''),
                curp=data.get('curp', '')
            )

            nuevo_empleado.save()

            return JsonResponse({'message': 'Empleado agregado correctamente.'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Error en el formato JSON de los datos.'}, status=400)
    else:
        return JsonResponse({'message': 'Error en la solicitud.'}, status=400)

@api_view(['GET'])
def get_empleados(request):
    empleados = Empleado.objects.all()
    serializer = EmpleadoSerializer(empleados, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def obtener_datos_empleado(request, empleado_id):
    print("Empleado ID recibido:", empleado_id)
    try:
        empleado = Empleado.objects.get(pk=empleado_id)
        serializer = EmpleadoSerializer(empleado)
        return JsonResponse(serializer.data)
    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)

    

@api_view(['GET'])
def empleados_con_registros(request, *args, **kwargs):
    try:
        empleados_con_registros = Empleado.objects.annotate(
            num_prestamos=Count('prestamos'),
            num_seguros_vida=Count('seguros_vida')
        ).filter(Q(num_prestamos__gt=0) | Q(num_seguros_vida__gt=0))

        serializer = EmpleadoSerializer(empleados_con_registros, many=True)

        data = serializer.data
        for index, empleado_data in enumerate(data):
            empleado_id = empleado_data['id']

            prestamos = PrestamoSerializer(Empleado.objects.get(pk=empleado_id).prestamos.all(), many=True).data
            seguros_vida = SeguroVidaSerializer(Empleado.objects.get(pk=empleado_id).seguros_vida.all(), many=True).data

            data[index]['prestamos'] = prestamos
            data[index]['seguros_vida'] = seguros_vida

       
        return Response(data)
    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['GET'])
def obtener_detalles_seguro_vida_por_empleado(request, empleado_id, *args, **kwargs):
    try:
        detalle_seguro_vida = SeguroVida.objects.get(empleado_id=empleado_id)
        serializer = SeguroVidaSerializer(detalle_seguro_vida)
        return Response(serializer.data)
    except SeguroVida.DoesNotExist:
        return Response({"error": "Detalle de seguro de vida no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def obtener_detalles_prestamo_por_empleado(request, empleado_id, *args, **kwargs):
    try:
        detalle_prestamo = Prestamo.objects.get(empleado_id=empleado_id)
        serializer = PrestamoSerializer(detalle_prestamo)
        return Response(serializer.data)
    except Prestamo.DoesNotExist:
        return Response({"error": "Detalle de préstamo no encontrado"}, status=status.HTTP_404_NOT_FOUND)


def get_empleados_con_registros(request):
    empleados_con_registros = [...] 
    return JsonResponse(empleados_con_registros, safe=False)

def eliminar_registro_prestamo(request, registro_id):
    # Lógica para eliminar un registro de préstamo
    registro_prestamo = get_object_or_404(Prestamo, id=registro_id)
    registro_prestamo.delete()
    return JsonResponse({'mensaje': 'Registro de préstamo eliminado correctamente'})

def eliminar_registro_seguro_vida(request, registro_id):
    # Lógica para eliminar un registro de seguro de vida
    registro_seguro_vida = get_object_or_404(SeguroVida, id=registro_id)
    registro_seguro_vida.delete()
    return JsonResponse({'mensaje': 'Registro de seguro de vida eliminado correctamente'})

@api_view(['GET'])
def GastosFunerariosView(request, empleado_id, *args, **kwargs):
    try:
        gastos_funerarios = GastosFunerarios.objects.get(empleado_id=empleado_id)
        serializer = GastosFunerariosSerializer(gastos_funerarios)
        return Response(serializer.data)
    except GastosFunerarios.DoesNotExist:
        return Response({"error": "Detalles de gastos funerarios no encontrados"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def guardar_gastos_funerarios(request):
    if request.method == 'POST':
        datos_gastos_funerarios = request.data
        serializer = GastosFunerariosSerializer(data=datos_gastos_funerarios)

        if serializer.is_valid():
            empleado_id = datos_gastos_funerarios.get('empleado_id')

            try:
                empleado = Empleado.objects.get(pk=empleado_id)
            except Empleado.DoesNotExist:
                return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(empleado=empleado)
            return Response({'mensaje': 'Gastos funerarios registrados correctamente'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Datos de gastos funerarios no válidos'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
def aprobar_prestamo(request, empleado_id):
    if request.method == 'POST':
        try:
            prestamo = Prestamo.objects.get(empleado_id=empleado_id, aprobado=False)

            prestamo.estatus = 'aprobado'
            prestamo.save()

            prestamo_aprobado = PrestamoAprobado(
                empleado=prestamo.empleado,
                cantidad=prestamo.cantidad,
                quincenas=prestamo.quincenas,
            )

            prestamo_aprobado.save()

            return JsonResponse({'message': 'Préstamo aprobado correctamente.'})
        except Prestamo.DoesNotExist:
            return JsonResponse({'error': 'Préstamo no encontrado o ya aprobado.'}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    

    
@api_view(['GET'])
def obtener_detalles_prestamo_aprobado(request, *args, **kwargs):
    try:
        detalles_prestamo_aprobado = PrestamoAprobado.objects.all()
        serializer = PrestamoAprobadoSerializer(detalles_prestamo_aprobado, many=True)
        return Response(serializer.data)
    except PrestamoAprobado.DoesNotExist:
        return Response({"error": "Detalles de préstamo aprobado no encontrados"}, status=status.HTTP_404_NOT_FOUND)
