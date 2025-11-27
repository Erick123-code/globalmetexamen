# from rest_framework import viewsets
# from .serializer import ProgrammerSerializer
# from .models import Programmer  
# # Create your views here.

# class ProgrammerViewSet(viewsets.ModelViewSet):
#     queryset = Programmer.objects.all()
#     serializer_class = ProgrammerSerializer
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import json
import pandas as pd
import csv
import requests

class EstadisticasTemperatura(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/estadisticas/temperatura/?dia=2025-11-23&unidad=fahrenheit"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            
            unidad = request.GET.get('unidad')
            unidad_description = unidad
            if not unidad:
                unidad = 'temperatura_c'
                unidad_description = 'celsius'
            else:
                if unidad == 'celsius':
                    unidad = 'temperatura_c'
                if unidad == 'fahrenheit':
                    unidad = 'temperatura_f'
                    
                if unidad_description != 'celsius' and unidad_description != 'fahrenheit':
                    return JsonResponse({
                    "estado": "error",
                    "datos": "valor debe de ser celsius o fahrenheit"    
                    })
            datos_ordenados_asc = sorted(response.json(), key=lambda x: x[unidad])
            datos_ordenados_desc = sorted(response.json(), key=lambda x: x[unidad], reverse=True)
            temperaturas = [dato[unidad] for dato in response.json() if dato[unidad] is not None]
            promedio = sum(temperaturas) / len(temperaturas) if temperaturas else 0
            datos = {'minimo': str(datos_ordenados_asc[0][unidad]) + " " +unidad_description, 'maximo': str(datos_ordenados_desc[0][unidad])  + " " + unidad_description, 'promedio': str(promedio)  + " " + unidad_description}
            return JsonResponse({
                "estado": "éxito",
                "mensaje": "Temperatura",
                "datos": datos if datos else []    
            })
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)

class EstadisticasHumedad(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/estadisticas/humedad/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            
            datos_ordenados_asc = sorted(response.json(), key=lambda x: x['humedad_relativa'])
            datos_ordenados_desc = sorted(response.json(), key=lambda x: x['humedad_relativa'], reverse=True)
            humedad = [dato['humedad_relativa'] for dato in response.json() if dato['humedad_relativa'] is not None]
            promedio = sum(humedad) / len(humedad) if humedad else 0
            datos = {'minimo': datos_ordenados_asc[0]['humedad_relativa'], 'maximo': datos_ordenados_desc[0]['humedad_relativa'], 'promedio': promedio}
            return JsonResponse({
                "estado": "éxito",
                "mensaje": "Humedad",
                "datos": datos if datos else []    
            })
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)
            
class EstadisticasViento(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/estadisticas/viento/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            
            datos_ordenados_asc = sorted(response.json(), key=lambda x: x['viento_kmh'])
            datos_ordenados_desc = sorted(response.json(), key=lambda x: x['viento_kmh'], reverse=True)
            viento = [dato['viento_kmh'] for dato in response.json() if dato['viento_kmh'] is not None]
            promedio = sum(viento) / len(viento) if viento else 0
            datos = {'minimo': datos_ordenados_asc[0]['viento_kmh'], 'maximo': datos_ordenados_desc[0]['viento_kmh'], 'promedio': promedio}
            return JsonResponse({
                "estado": "éxito",
                "mensaje": "Viento",
                "datos": datos if datos else []    
            })
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)
            
class EstadisticasRafaga(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/estadisticas/rafaga/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            
            datos_ordenados_asc = sorted(response.json(), key=lambda x: x['viento_rafaga_kmh'])
            datos_ordenados_desc = sorted(response.json(), key=lambda x: x['viento_rafaga_kmh'], reverse=True)
            rafaga = [dato['viento_rafaga_kmh'] for dato in response.json() if dato['viento_rafaga_kmh'] is not None]
            promedio = sum(rafaga) / len(rafaga) if rafaga else 0
            datos = {'minimo': datos_ordenados_asc[0]['viento_rafaga_kmh'], 'maximo': datos_ordenados_desc[0]['viento_rafaga_kmh'], 'promedio': promedio}
            return JsonResponse({
                "estado": "éxito",
                "mensaje": "Ráfaga",
                "datos": datos if datos else []    
            })
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)
            
class EstadisticasPresion(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/estadisticas/presion/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            
            datos_ordenados_asc = sorted(response.json(), key=lambda x: x['presion_mb'])
            datos_ordenados_desc = sorted(response.json(), key=lambda x: x['presion_mb'], reverse=True)
            precion = [dato['presion_mb'] for dato in response.json() if dato['presion_mb'] is not None]
            promedio = sum(precion) / len(precion) if precion else 0
            datos = {'minimo': datos_ordenados_asc[0]['presion_mb'], 'maximo': datos_ordenados_desc[0]['presion_mb'], 'promedio': promedio}
            return JsonResponse({
                "estado": "éxito",
                "mensaje": "Preción",
                "datos": datos if datos else []    
            })
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)

class ResumenDiario(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/resumen/diario/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            unidad = 'celsius'
            unidad_description = unidad
            unidad = 'temperatura_c'
            temperaturas_datos = response.json()
            datos_ordenados_asc_temperatura = sorted(temperaturas_datos, key=lambda x: x[unidad])
            datos_ordenados_desc_temperatura = sorted(temperaturas_datos, key=lambda x: x[unidad], reverse=True)
            temperaturas = [dato[unidad] for dato in temperaturas_datos if dato[unidad] is not None]
            promedio_temperatura = sum(temperaturas) / len(temperaturas) if temperaturas else 0
            datos = []
            #se agrega temperatura
            datos.append({"temperatura": {'minimo': str(datos_ordenados_asc_temperatura[0][unidad]) + " " +unidad_description, 'maximo': str(datos_ordenados_desc_temperatura[0][unidad])  + " " + unidad_description, 'promedio': str(promedio_temperatura)  + " " + unidad_description}})
            #se agrega humedad
            humedades = response.json()
            datos_ordenados_asc_humedad = sorted(humedades, key=lambda x: x['humedad_relativa'])
            datos_ordenados_desc_humedad = sorted(humedades, key=lambda x: x['humedad_relativa'], reverse=True)
            humedad = [dato['humedad_relativa'] for dato in humedades if dato['humedad_relativa'] is not None]
            promedio_humedad = sum(humedad) / len(humedad) if humedad else 0
            datos.append({"humedad": {'minimo': datos_ordenados_asc_humedad[0]['humedad_relativa'], 'maximo': datos_ordenados_desc_humedad[0]['humedad_relativa'], 'promedio': promedio_humedad}})
            #se agrega viento
            vientos = response.json()
            datos_ordenados_asc_viento = sorted(vientos, key=lambda x: x['viento_kmh'])
            datos_ordenados_desc_viento = sorted(vientos, key=lambda x: x['viento_kmh'], reverse=True)
            viento = [dato['viento_kmh'] for dato in vientos if dato['viento_kmh'] is not None]
            promedio_viento = sum(viento) / len(viento) if viento else 0
            datos.append({"viento": {'minimo': datos_ordenados_asc_viento[0]['viento_kmh'], 'maximo': datos_ordenados_desc_viento[0]['viento_kmh'], 'promedio': promedio_viento}})
            #se agrega rafaga
            rafagas = response.json()
            datos_ordenados_asc_rafaga = sorted(rafagas, key=lambda x: x['viento_rafaga_kmh'])
            datos_ordenados_desc_rafaga = sorted(rafagas, key=lambda x: x['viento_rafaga_kmh'], reverse=True)
            rafaga = [dato['viento_rafaga_kmh'] for dato in rafagas if dato['viento_rafaga_kmh'] is not None]
            promedio_rafaga = sum(rafaga) / len(rafaga) if rafaga else 0
            datos.append({"rafaga": {'minimo': datos_ordenados_asc_rafaga[0]['viento_rafaga_kmh'], 'maximo': datos_ordenados_desc_rafaga[0]['viento_rafaga_kmh'], 'promedio': promedio_rafaga}})
            #se agrega presion
            presiones = response.json()
            datos_ordenados_asc_presion = sorted(presiones, key=lambda x: x['presion_mb'])
            datos_ordenados_desc_presion = sorted(presiones, key=lambda x: x['presion_mb'], reverse=True)
            presion = [dato['presion_mb'] for dato in presiones if dato['presion_mb'] is not None]
            promedio_presion = sum(presion) / len(presion) if presion else 0
            datos.append({"presion": {'minimo': datos_ordenados_asc_presion[0]['presion_mb'], 'maximo': datos_ordenados_desc_presion[0]['presion_mb'], 'promedio': promedio_presion}})
            return JsonResponse({
                "estado": "éxito",
                "mensaje": "Resumen Diario",
                "datos": datos if datos else []    
            })
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)

class ExportarEstadisticas(View):
    def get(self, request):
        
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/exportar/estadisticas/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
            
            unidad = 'celsius'
            unidad_description = unidad
            unidad = 'temperatura_c'
            temperaturas_datos = response.json()
            datos_ordenados_asc_temperatura = sorted(temperaturas_datos, key=lambda x: x[unidad])
            datos_ordenados_desc_temperatura = sorted(temperaturas_datos, key=lambda x: x[unidad], reverse=True)
            temperaturas = [dato[unidad] for dato in temperaturas_datos if dato[unidad] is not None]
            promedio_temperatura = sum(temperaturas) / len(temperaturas) if temperaturas else 0
            datos = []
            #se agrega temperatura
            datos.append({'medida':"temperatura",'minimo': str(datos_ordenados_asc_temperatura[0][unidad]) + " " +unidad_description, 'maximo': str(datos_ordenados_desc_temperatura[0][unidad])  + " " + unidad_description, 'promedio': str(promedio_temperatura)  + " " + unidad_description})
            #se agrega humedad
            humedades = response.json()
            datos_ordenados_asc_humedad = sorted(humedades, key=lambda x: x['humedad_relativa'])
            datos_ordenados_desc_humedad = sorted(humedades, key=lambda x: x['humedad_relativa'], reverse=True)
            humedad = [dato['humedad_relativa'] for dato in humedades if dato['humedad_relativa'] is not None]
            promedio_humedad = sum(humedad) / len(humedad) if humedad else 0
            datos.append({'medida':'humedad','minimo': datos_ordenados_asc_humedad[0]['humedad_relativa'], 'maximo': datos_ordenados_desc_humedad[0]['humedad_relativa'], 'promedio': promedio_humedad})
            #se agrega viento
            vientos = response.json()
            datos_ordenados_asc_viento = sorted(vientos, key=lambda x: x['viento_kmh'])
            datos_ordenados_desc_viento = sorted(vientos, key=lambda x: x['viento_kmh'], reverse=True)
            viento = [dato['viento_kmh'] for dato in vientos if dato['viento_kmh'] is not None]
            promedio_viento = sum(viento) / len(viento) if viento else 0
            datos.append({'medida':'viento','minimo': datos_ordenados_asc_viento[0]['viento_kmh'], 'maximo': datos_ordenados_desc_viento[0]['viento_kmh'], 'promedio': promedio_viento})
            #se agrega rafaga
            rafagas = response.json()
            datos_ordenados_asc_rafaga = sorted(rafagas, key=lambda x: x['viento_rafaga_kmh'])
            datos_ordenados_desc_rafaga = sorted(rafagas, key=lambda x: x['viento_rafaga_kmh'], reverse=True)
            rafaga = [dato['viento_rafaga_kmh'] for dato in rafagas if dato['viento_rafaga_kmh'] is not None]
            promedio_rafaga = sum(rafaga) / len(rafaga) if rafaga else 0
            datos.append({'medida':'rafaga','minimo': datos_ordenados_asc_rafaga[0]['viento_rafaga_kmh'], 'maximo': datos_ordenados_desc_rafaga[0]['viento_rafaga_kmh'], 'promedio': promedio_rafaga})
            #se agrega presion
            presiones = response.json()
            datos_ordenados_asc_presion = sorted(presiones, key=lambda x: x['presion_mb'])
            datos_ordenados_desc_presion = sorted(presiones, key=lambda x: x['presion_mb'], reverse=True)
            presion = [dato['presion_mb'] for dato in presiones if dato['presion_mb'] is not None]
            promedio_presion = sum(presion) / len(presion) if presion else 0
            datos.append({'medida':'presion','minimo': datos_ordenados_asc_presion[0]['presion_mb'], 'maximo': datos_ordenados_desc_presion[0]['presion_mb'], 'promedio': promedio_presion})
        
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="datos_meteorologicos_estadisticas_2025_11_2024.csv"'
            
            if datos:
                # Convertir a DataFrame y luego a CSV
                df = pd.DataFrame(datos)
                df.to_csv(response, index=False)
            else:
                writer = csv.writer(response)
                writer.writerow(['No hay datos disponibles'])
            
            return response
            
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)

class ExportarMediciones(View):
    def get(self, request):
        try:
            fecha = request.GET.get('dia')
            if not fecha:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Ingrese parametro dia por metodo GET ejemplo http://127.0.0.1:8000/api/meteorologia/exportar/mediciones/?dia=2025-11-23"    
                })
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                return JsonResponse({
                    "estado": "error",
                    "datos": "Formato de fecha inválido. Use AAAA-MM-DD."    
                })
            url = f"https://data.globalmet.mx/api/mediciones/perday/estacion/689/?dia={fecha}"
            access_token = "Token 2c9f700c179a5f18f501167ea286e4203fffc289"

            # 2. Crea el diccionario de encabezados (headers)
            headers = {
                "Content-Type": "application/json",
                "Authorization": access_token
            }

            # 3. Realiza la petición GET
            response = requests.get(url, headers=headers)
                
            datos = response.json()
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="datos_meteorologicos_mediciones_2025_11_24.csv"'
            
            if datos:
                # Convertir a DataFrame y luego a CSV
                df = pd.DataFrame(datos)
                df.to_csv(response, index=False)
            else:
                writer = csv.writer(response)
                writer.writerow(['No hay datos disponibles'])
            
            return response
        
        except Exception as e:
            return JsonResponse({
                "estado": "error",
                "mensaje": str(e)
            }, status=500)
            

# Vista para página web
def pagina_principal(request):
    return render(request, 'meteorologia/index.html')