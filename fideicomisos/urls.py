
from fideicomisos_backend import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'fideicomisos_backend'

urlpatterns  = [
   # path('api/empleados/', views.empleado, name='empleados'),
    path('guardar_formulario/', views.guardar_formulario, name='guardar_formulario'),
    path('admin/', admin.site.urls),
    path('agregar_empleado/', views.agregar_empleado, name='agregar_empleado'),
    path('tabla-empleado/', views.get_empleados, name='tabla_empleado'),
    path('guardar-gastos-funerarios/', views.guardar_gastos_funerarios, name='guardar_gastos_funerarios'),
    path('guardarSeguroVida/', views.registrar_seguros_vida, name='guardar_seguro_vida'),
    path('datos-empleado/<int:empleado_id>/', views.obtener_datos_empleado, name='obtener_datos_empleado'),
    path('empleados-con-registros/', views.empleados_con_registros, name='empleados-con-registros'),
    path('seguros-vida/<int:empleado_id>/', views.obtener_seguros_vida_por_empleado, name='detalles_seguro_vida_por_empleadoe'),
    path('prestamos/<int:empleado_id>/', views.obtener_detalles_prestamo_por_empleado, name='detalles_prestamo_por_empleado'),
    path('eliminar-registro-prestamo/<int:registro_id>/', views.eliminar_registro_prestamo, name='eliminar-registro-prestamo'),
    path('eliminar-registro-seguro-vida/<int:registro_id>/', views.eliminar_registro_seguro_vida, name='eliminar-registro-seguro-vida'),
    path('gastos-funerarios/<int:empleado_id>/', views.gastos_funerarios_view, name='gastos_funerarios'),
    path('prestamos/<int:prestamo_id>/aprobar/', views.aprobar_prestamo, name='aprobar_prestamo'),
    path('prestamos/aprobados/', views.obtener_registros_aprobados, name='obtener_registros_aprobados'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('prestamos/empleado/<int:empleado_id>/actualizar/', views.actualizar_prestamo_por_empleado, name='actualizar_prestamo_por_empleado'),
    # path('prestamos/<int:empleado_id>/aprobar/', views.aprobar_prestamo_por_empleado, name='aprobar_prestamo_por_empleado'),
    path('prestamos/<int:prestamo_id>/actualizar/', views.actualizar_prestamo, name='actualizar-prestamo'), 
    path('seguros-vida/<int:seguro_vida_id>/actualizar/', views.actualizar_seguro_vida, name='actualizar_seguro_vida'),
    path('registrar_empleado/', views.registrar_empleado, name='registrar empleado'),
    # path('api/empleado/<int:id>/', views.obtener_empleado, name='obtener_empleado'),
    path('buscar-empleado/<str:nombreCompleto>/', views.buscar_empleado_por_nombre, name='buscar_empleado_por_nombre_completo'),
    path('empleados/<int:empleado_id>/solicitar-jubilacion/', views.solicitar_jubilacion, name='solicitar_jubilacion'),
] 