from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_principal, name='inicio'),
    path('/estadisticas/temperatura/', views.EstadisticasTemperatura.as_view(), name='estadisitcas_temperatura'),
    path('/estadisticas/humedad/', views.EstadisticasHumedad.as_view(), name='estadisticas_humedad'),
    path('/estadisticas/viento/', views.EstadisticasViento.as_view(), name='estadisticas_viento'),
    path('/estadisticas/rafaga/', views.EstadisticasRafaga.as_view(), name='estadisticas_rafaga'),
    path('/estadisticas/presion/', views.EstadisticasPresion.as_view(), name='estadisticas_presion'),
    path('/resumen/diario/', views.ResumenDiario.as_view(), name='estadisticas_diario'),
    path('/exportar/estadisticas/', views.ExportarEstadisticas.as_view(), name='exportar_estadisticas'),
    path('/exportar/mediciones/', views.ExportarMediciones.as_view(), name='exportar_mediciones'),
]