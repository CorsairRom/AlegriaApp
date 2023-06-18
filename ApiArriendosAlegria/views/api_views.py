from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse

from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ApiArriendosAlegria.utils import GetfechaScl

from ApiArriendosAlegria.models import (
    Usuario,
    Trabajador,
    TipoTrabajador,
    Region,
    Comuna,
    Banco,
    TipoCuenta,
    Cuenta,
    Propiedad,
    TipoPropiedad,
    Propietario,
    PersonalidadJuridica,
    Arrendatario,
    Arriendo,
    DetalleArriendo,
    Gastocomun,
    ServiciosExtras,
    ArriendoDepartamento,
    ValoresGlobales,
    CodigoPropiedad
)
from ApiArriendosAlegria.serializers.base_serializers import (
    SerializadorUsuario,
    SerializerArrendatarioArriendo,
    SerializerArriendoDepartamento,
    SerializerTablaArriendo,
    SerializerTrabajador,
    SerializerTipoTrabajado,
    SerializerRegion,
    SerializerComuna,
    SerializerBanco,
    SerializerTipoCuenta,
    SerializerCuenta,
    SerializerPropiedad,
    SerializerPersonalidadJuridica,
    SerializerTipoPropiedad,
    SerializerPropietario,
    SerializerArrendatario,
    SerializerArriendo,
    SerializerDetalleArriendo,
    SerializerGastoComun,
    SerializerServiciosExtas,
    SerializerValoresGlobales,
    SerializerActualizarValorArriendo,
    SerializerArriendoConDetalles,
    ListadoCodigoPropiedadSerializer,
)

from ApiArriendosAlegria.permission import IsStaffUser
from ApiArriendosAlegria.authentication_mixins import Authentication
from django.template.loader import get_template
from xhtml2pdf import pisa

# -------------Api Bancos---------------
class BancoViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerBanco
    queryset = Banco.objects.all()


# -------------Api Tipo Cuentas Bancarias---------------
class TipoCuentaBancariaViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SerializerTipoCuenta
    queryset = TipoCuenta.objects.all()


# -------------Api TypeWorkers---------------
class TypeWorkerViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTipoTrabajado
    queryset = TipoTrabajador.objects.all()


# -------------Api Worker---------------
class TrabajadorViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTrabajador
    queryset = Trabajador.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut_trab', 'pri_nom_trab']

    
# -------------Api Regiones--------------- 
class RegionReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    queryset = Region.objects.all()
    serializer_class = SerializerRegion
    filter_backends = [DjangoFilterBackend]


# -------------Api Communes---------------   
class ComunaReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    queryset = Comuna.objects.all()
    serializer_class = SerializerComuna
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reg_id']


# --- API Usuario (nuevo) ---
class UsuarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializadorUsuario
    queryset = Usuario.objects.all()


# ---------------------Segundo sprint-------------------
class PropietarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPropietario
    queryset = Propietario.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut_prop','pri_nom_prop','pri_ape_prop']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.personalidad_juridica:
            instance.personalidad_juridica.delete()
            
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

        
    
    
class PersonalidadJuridicaViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPersonalidadJuridica
    queryset = PersonalidadJuridica.objects.all()


class CuentaViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerCuenta
    queryset = Cuenta.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cuenta','propietario_rut']

class PropiedadViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPropiedad
    queryset = Propiedad.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['propietario']

    @action(detail=False, methods=['get'])
    def con_codigo(self, request):
        codigos = CodigoPropiedad.objects.all().order_by('cod')
        serializer = ListadoCodigoPropiedadSerializer(codigos, many=True)
        return Response(serializer.data)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TipoPropiedadViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTipoPropiedad
    queryset = TipoPropiedad.objects.all()

class ArriendatarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArrendatario
    queryset = Arrendatario.objects.all()
    
    @action(detail=True, methods=['get'])
    def detalle(self, request, pk=None):
        arrendatario = self.get_object()
        serializer = SerializerArrendatarioArriendo(arrendatario)
        
        return Response(serializer.data)
        
    
    



    
class ArriendoViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArriendo
    queryset = Arriendo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado_arriendo','propiedad']

    def get_serializer_class(self):
        if self.action == 'list':
            return SerializerTablaArriendo
        if self.action == 'retrieve':
            return SerializerArriendoConDetalles
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        propiedad_id = request.data.get('propiedad_id', None)
        arrendatario_id = request.data.get('arrendatario_id', None)

        if propiedad_id is not None:
            try:
                propiedad = Propiedad.objects.get(pk = propiedad_id)
                if propiedad.esta_en_arriendo():
                    return Response({'error' : "La propiedad ya registra un arriendo activo"}, status=404)
            except:
                pass

        if arrendatario_id is not None:
            try:
                arrendatario = Arrendatario.objects.get(pk = arrendatario_id)
                if arrendatario.tiene_un_arriendo_activo():
                    return Response({'error' : "El Arrendatario ya registra un arriendo activo"}, status=404)
            except:
                pass


        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
class ArriendoDepartamentoViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArriendoDepartamento
    queryset = ArriendoDepartamento.objects.all()
    


class DashboardViewSet(viewsets.GenericViewSet):
    queryset = DetalleArriendo.objects.all() 
    serializer_class = SerializerDetalleArriendo
    
    @action(detail=False, methods=['get'])
    def info(self, request):
        
        today = GetfechaScl()

        try:
            detalle_arriendo = self.get_queryset().filter(fecha_a_pagar__month = today.month , fecha_a_pagar__year = today.year).order_by('fecha_a_pagar')
            propiedades_con_reajuste = detalle_arriendo.filter(toca_reajuste = True).count()
            total_arriendos_mes = detalle_arriendo.count()
            total_arriendos_pagados = 0
            total_arriendos_por_pagar = 0
            
            arriendo_atrazados = []
            
            for detalle in detalle_arriendo:
                if detalle.fecha_pagada != None:
                    total_arriendos_pagados += 1
                else:
                    total_arriendos_por_pagar += 1
                    propiedad_cod = detalle.arriendo.propiedad.cod
                    arrendatarios_nom = detalle.arriendo.arrendatario.get_name()
                    fecha_pago = detalle.fecha_a_pagar
                    propiedad_id = detalle.arriendo.propiedad.id
                    dias_atrazo = today.day - fecha_pago.day
                    if dias_atrazo > 0:
                        atrasados = {
                            'propiedad_cod' : propiedad_cod,
                            'arrendatarios_nom' : arrendatarios_nom,
                            'fecha_pago' : fecha_pago,
                            'dias_atraso' : dias_atrazo,
                            'propiedad_id': propiedad_id
                        }
                        arriendo_atrazados.append(atrasados)
            
            total_propiedades = Propiedad.objects.count()
            total_arriendos = Arriendo.objects.count()
            sin_arrendar = total_propiedades - total_arriendos
            
            data = {
                "total_arriendos_mes": total_arriendos_mes,
                "total_arriendos_pagados" : total_arriendos_pagados,
                "total_arriendos_por_pagar" :total_arriendos_por_pagar,
                "propiedades_con_reajuste" : propiedades_con_reajuste, 
                "total_propiedades" : total_propiedades,
                "total_arriendos" : total_arriendos,
                "sin_arrendar": sin_arrendar,
                "atrasados" : arriendo_atrazados  
            }
        except:
            data = {
                "total_arriendos_mes": 0,
                "total_arriendos_pagados" : 0,
                "total_arriendos_por_pagar" :0,
                "propiedades_con_reajuste" : 0, 
                "total_propiedades" : 0,
                "total_arriendos" : 0,
                "sin_arrendar": 0,
                "atrasados" : []     
            }
        
        return Response(data)
    



class DetalleArriendoViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerDetalleArriendo
    queryset = DetalleArriendo.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['arriendo']
  
  
    @action(detail=True, methods=['post'])
    def calcular_multa_arriendo(self, request, pk=None):
        detalle_arriendo = self.get_object()
        tasa_multa = ValoresGlobales.objects.get(id=1).valor / 100 # 0.33% de multa por día
        fecha_a_pagar = detalle_arriendo.fecha_a_pagar
        monto_a_pagar = detalle_arriendo.monto_a_pagar
        today = timezone.now()
        print(f"today = {today}")

        if today > fecha_a_pagar:
            if fecha_a_pagar.day <= 5:
                # Obtener el primer día del mes actual
                first_day_month = today.replace(day=1)
                print(f"first_day_month = {first_day_month}")

                # Calcular la diferencia de días entre el primer día del mes actual y la fecha actual
                dias_pasados = (today - first_day_month).days
            else:
                # En caso que el día de pago sea, por ejemplo, el día 20 del mes
                dias_pasados = (today - fecha_a_pagar).days
        
        print(f"dias_pasados = {dias_pasados}")
        # Calcular el valor de la multa
        valor_multa = monto_a_pagar * tasa_multa * dias_pasados

        detalle_arriendo.valor_multa = valor_multa
        detalle_arriendo.save(update_fields=["valor_multa"])

        detalle_arriendo_serializer = SerializerDetalleArriendo(detalle_arriendo)

        return Response(
            data=detalle_arriendo_serializer.data,
            status=status.HTTP_200_OK
            )

class ServiciosExtrasViewSet(viewsets.ModelViewSet):
    """
    Vista "Servicios Extra".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerServiciosExtas
    queryset = ServiciosExtras.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['propiedad']
    
class GastoComunViewSet(viewsets.ModelViewSet):
    """
    Vista "Gastos Comun".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerGastoComun
    queryset = Gastocomun.objects.all()
    
    
class ValoresGlobalesViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerValoresGlobales
    queryset = ValoresGlobales.objects.all()


class ActualizarValorArriendoPropiedad(viewsets.GenericViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerActualizarValorArriendo

    def create(self, request, *args, **kwargs):
        serializer = SerializerActualizarValorArriendo(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.data

        try:
            arriendo = Arriendo.objects.get(pk=data.get('arriendo_id'))
        except:
            return Response({'error': 'El Arriendo no existe'},
                        status=status.HTTP_404_NOT_FOUND)

        arriendo.valor_arriendo = data.get("nuevo_valor_arriendo")

        if data.get("por_reajuste") == True:
            nueva_fecha_reajuste = arriendo.fecha_reajuste + relativedelta(months=arriendo.periodo_reajuste)
        else:
            nueva_fecha_reajuste = datetime.utcnow() + relativedelta(months=arriendo.periodo_reajuste)

        arriendo.fecha_reajuste = nueva_fecha_reajuste

        arriendo.save(update_fields=["valor_arriendo", "fecha_reajuste"])

        arriendo_serializer = SerializerArriendo(arriendo)
        return Response(
            status=status.HTTP_200_OK, 
            data=arriendo_serializer.data
        )

class Reportes(viewsets.GenericViewSet):
    
    
    
    def list(self, request):
        try:
            
            template_path = '../templates/reporte.html'
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            template = get_template(template_path)
            context = {'msg': 'Hola mundo'}
            html = template.render(context)
            pisa_status = pisa.CreatePDF(html, dest=response)
        except:
            pass
                
        
        return  response


