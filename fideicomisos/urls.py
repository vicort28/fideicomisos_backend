
from fideicomisos_backend import views
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

app_name = 'fideicomisos_backend'

urlpatterns  = [
   # path('api/empleados/', views.empleado, name='empleados'),
    path('guardar_formulario/', views.guardar_formulario, name='guardar_formulario'),
    path('admin/', admin.site.urls),
    path('agregar_empleado/', views.agregar_empleado, name='agregar_empleado'),
    path('tabla-empleado/', views.get_empleados, name='tabla_empleado'),
    path('gastos-funerarios/', views.guardar_gastos_funerarios, name='gastos_funerarios'),
    path('guardarSeguroVida/', views.guardar_seguro_vida, name='guardar_seguro_vida'),
    path('datos-empleado/<int:empleado_id>/', views.obtener_datos_empleado, name='obtener_datos_empleado'),
    path('empleados-con-registros/', views.empleados_con_registros, name='empleados-con-registros'),
    path('seguros-vida/<int:empleado_id>/', views.obtener_detalles_seguro_vida_por_empleado, name='detalles_seguro_vida_por_empleado'),
    path('prestamos/<int:empleado_id>/', views.obtener_detalles_prestamo_por_empleado, name='detalles_prestamo_por_empleado'),
    path('empleados-con-registros/', views.get_empleados_con_registros, name='empleados-con-registros'),
    path('eliminar-registro-prestamo/<int:registro_id>/', views.eliminar_registro_prestamo, name='eliminar-registro-prestamo'),
    path('eliminar-registro-seguro-vida/<int:registro_id>/', views.eliminar_registro_seguro_vida, name='eliminar-registro-seguro-vida'),
    path('gastos-funerarios/<int:empleado_id>/', views.GastosFunerariosView, name='gastos_funerarios'),
    path('empleados/<int:empleado_id>/aprobacion-prestamo/', views.aprobar_prestamo, name='aprobar_prestamo'),
    path('aprobacion-prestamo/', views.obtener_detalles_prestamo_aprobado, name='aprobar_prestamo'),
] 