from collections import Counter
from datetime import timezone
import traceback
from django.http import JsonResponse
from .models import Prestamo, SeguroVida, GastosFunerarios
from .models import Empleado
from rest_framework.decorators import api_view
from .serializers import  PrestamoSerializer, EmpleadoSerializer, SeguroVidaSerializer, GastosFunerariosSerializer
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
from rest_framework import generics
from django.db import transaction



# Django view
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prestamo, Empleado
from .serializers import PrestamoSerializer

# views.py
from rest_framework import viewsets
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

        if not empleado_id:
            return JsonResponse({'error': 'empleado_id es requerido'}, status=400)

        try:
            empleado = Empleado.objects.get(id=empleado_id)
        except Empleado.DoesNotExist:
            return JsonResponse({'error': 'El empleado no existe'}, status=404)

        # Asignar el empleado encontrado al campo de empleado en lugar de modificar el id directamente
        datos_formulario1['empleado'] = empleado.id

        serializer = PrestamoSerializer(data=datos_formulario1)

        if serializer.is_valid():
            prestamo = serializer.save()

            cantidad = float(prestamo.cantidad.replace('$', '').replace(',', ''))
            quincenas = float(prestamo.quincenas)
            prestamo.pagoporquincena = cantidad / quincenas
            prestamo.save()

            return JsonResponse({'mensaje': 'Datos del formulario guardados correctamente'}, status=201)
        else:
            return JsonResponse({'error': 'Datos del formulario no válidos', 'detalles': serializer.errors}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer


@api_view(['POST'])
@csrf_exempt
def registrar_empleado(request):
    if request.method == 'POST':
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Empleado registrado correctamente'}, status=201)
        return Response(serializer.errors, status=400)


@api_view(['POST'])
def registrar_seguros_vida(request):
    empleado_id = request.data.get('empleado_id')
    seguros_data = request.data.get('seguros', [])

    if not empleado_id:
        return Response({'error': 'El empleado_id es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        empleado = Empleado.objects.get(id=empleado_id)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():  # Usar transacciones para asegurar consistencia
        for seguro_data in seguros_data:
            seguro_data['empleado'] = empleado.id  # Asociar el seguro al empleado
            serializer = SeguroVidaSerializer(data=seguro_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'mensaje': 'Seguros de vida registrados correctamente'}, status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def guardar_gastos_funerarios(request):
    if request.method == 'POST':
        empleado_id = request.data.get('empleado_id')
        padre = request.data.get('padre', False)
        madre = request.data.get('madre', False)
        hijo = request.data.get('hijo', False)
        esposo = request.data.get('esposo', False)
        
        # Aquí puedes realizar la lógica para guardar los datos en tu modelo de GastosFunerarios
        gastos_funerarios = GastosFunerarios.objects.create(
            empleado_id=empleado_id,
            padre=padre,
            madre=madre,
            hijo=hijo,
            esposo=esposo
        )

        gastos_funerarios.save()

        # Puedes devolver una respuesta con un mensaje de éxito
        return Response({'mensaje': 'Datos de gastos funerarios guardados correctamente'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@csrf_exempt
def agregar_empleado(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            nuevo_empleado = Empleado(
                nombres=data.get('nombres', ''),
                apellidoPaterno=data.get('apellidoPaterno', ''),
                apellidoMaterno=data.get('apellidoMaterno', ''),
                numeroEmpleado=data.get('numeroEmpleado', ''),
                telefono1=data.get('telefono', ''),
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
            num_prestamos=Count('prestamo'),
            num_seguros_vida=Count('seguros_vida'),
            num_gastos_funerarios=Count('gastos_funerarios')  # Contamos los gastos funerarios también
        ).filter(Q(num_prestamos__gt=0) | Q(num_seguros_vida__gt=0) | Q(num_gastos_funerarios__gt=0))

        serializer = EmpleadoSerializer(empleados_con_registros, many=True)

        data = serializer.data
        for index, empleado_data in enumerate(data):
            empleado_id = empleado_data['id']

            prestamos = PrestamoSerializer(Empleado.objects.get(pk=empleado_id).prestamo.all(), many=True).data
            seguros_vida = SeguroVidaSerializer(Empleado.objects.get(pk=empleado_id).seguros_vida.all(), many=True).data
            gastos_funerarios = GastosFunerariosSerializer(Empleado.objects.get(pk=empleado_id).gastos_funerarios.all(), many=True).data

            data[index]['prestamos'] = prestamos
            data[index]['seguros_vida'] = seguros_vida
            data[index]['gastos_funerarios'] = gastos_funerarios  # Añadimos los gastos funerarios

        return Response(data)
    except Exception as e:
        return Response({'error': str(e), 'traceback': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
def obtener_detalles_seguro_vida_por_empleado(request, empleado_id, *args, **kwargs):
    try:
        detalle_seguro_vida = SeguroVida.objects.filter(empleado_id=empleado_id)
        serializer = SeguroVidaSerializer(detalle_seguro_vida, many=True)
        return Response(serializer.data)
    except SeguroVida.DoesNotExist:
        return Response({"error": "Detalle de seguro de vida no encontrado"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def obtener_detalles_prestamo_por_empleado(request, empleado_id, *args, **kwargs):
    try:
        detalle_prestamo = Prestamo.objects.filter(numero_empleado=empleado_id)
        serializer = PrestamoSerializer(detalle_prestamo, many=True)
        return Response(serializer.data)
    except Prestamo.DoesNotExist:
        return Response({"error": "Detalle de préstamo no encontrado"}, status=status.HTTP_404_NOT_FOUND)


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
def gastos_funerarios_view(request, empleado_id):
    try:
        gastos_funerarios = GastosFunerarios.objects.filter(empleado_id=empleado_id)
        serializer = GastosFunerariosSerializer(gastos_funerarios, many=True)
        return Response(serializer.data)
    except GastosFunerarios.DoesNotExist:
        return Response({"error": "Detalles de gastos funerarios no encontrados"}, status=status.HTTP_404_NOT_FOUND)





# @csrf_exempt
# @api_view(['POST'])
# def aprobar_prestamo(request, prestamo_id):
#     if request.method == 'POST':
#         try:
#             prestamo = Prestamo.objects.get(id=prestamo_id)
#             if prestamo.aprobado:
#                 return JsonResponse({'error': 'Este préstamo ya ha sido aprobado'}, status=400)
#             prestamo.aprobado = True
#             prestamo.save()

#             prestamo_aprobado = PrestamoAprobado(
#                 empleado=prestamo.empleado,
#                 cantidad=prestamo.cantidad,
#                 quincenas=prestamo.quincenas,
#             )
#             prestamo_aprobado.save()

#             return JsonResponse({'message': 'Préstamo aprobado correctamente.'})
#         except Prestamo.DoesNotExist:
#             return JsonResponse({'error': 'Préstamo no encontrado.'}, status=404)
#     else:
#         return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
# @api_view(['POST'])
# def aprobar_prestamo_por_empleado(request, empleado_id):
#     try:
#         empleado = Empleado.objects.get(id=empleado_id)
#         prestamo = Prestamo.objects.filter(empleado=empleado, aprobado=False).first()
#         if prestamo:
#             prestamo.aprobado = True
#             prestamo.save()
#             return Response({"message": "Préstamo aprobado correctamente"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "No hay préstamos pendientes para este empleado"}, status=status.HTTP_404_NOT_FOUND)
#     except Empleado.DoesNotExist:
#         return Response({"message": "Empleado no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    
# @api_view(['GET'])
# def obtener_registros_aprobados(request):
#     prestamos_aprobados = Prestamo.objects.filter(aprobado=True)
#     serializer = PrestamoSerializer(prestamos_aprobados, many=True)
#     return Response(serializer.data)



@api_view(['PUT'])
def actualizar_prestamo(request, prestamo_id):
    try:
        prestamo = Prestamo.objects.get(pk=prestamo_id)
    except Prestamo.DoesNotExist:
        return Response({'error': 'Prestamo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PrestamoSerializer(prestamo, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def actualizar_seguro_vida(request, seguro_vida_id):
    try:
        seguro_vida = SeguroVida.objects.get(id=seguro_vida_id)
    except SeguroVida.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SeguroVidaSerializer(seguro_vida, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)