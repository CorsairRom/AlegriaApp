from enum import Enum
from django.db.models.signals import post_save, pre_save
from datetime import datetime
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta

from ApiArriendosAlegria.models import (
    Arriendo, 
    CodigoPropiedad, 
    DetalleArriendo, 
    Propiedad, 
    Propietario, 
    ServiciosExtras, 
    ValoresGlobales
)


class ValoreGlobalEnum(int, Enum):
    PORCENTAJE_MULTAS = 1
    IMPUESTO_HONORARIO = 2

@receiver(post_save, sender=Arriendo)
def _post_save_receiver(sender, instance, created, **kwargs):
    
    if created:
        
        propiedad = instance.propiedad

        # Se coloca el estado_arriendo en false en los arriendos de la propiedad del mismo arriendo que se está registrando
        # Igualmente está validado para no registrar una propiead en estado de arriendo True(Activo)
        propiedad.arriendo_set.all().filter(id=instance.id).update(estado_arriendo=False)


        # calculo de porcentaje comision y valor arriendo
        pctje_cobro_honorario = propiedad.propietario.pctje_cobro_honorario
        impuesto_honorario = ValoresGlobales.objects.get(pk=ValoreGlobalEnum.IMPUESTO_HONORARIO) # Ver cual es el ID correcto

        porc_comision = (pctje_cobro_honorario * (impuesto_honorario.valor / 100)) + pctje_cobro_honorario

        # Se establecen los valores del arriendo
        instance.estado_arriendo = True
        instance.comision = porc_comision
        instance.valor_arriendo = (propiedad.valor_arriendo_base * (instance.comision / 100)) + propiedad.valor_arriendo_base
        
        # calculo de fechas de pago para el arriendo
        fechas_pago = []
        for i in range(1, 13):
            #4 periodos cada 3meses
            if i == 1:
                fecha_inicio = instance.fecha_inicio
            else:
                fecha_inicio = instance.fecha_inicio + relativedelta(months=i-1)
            fecha_pago = fecha_inicio.replace(day=instance.dia_pago)
           
            detalle_arriendo = DetalleArriendo(arriendo = instance, fecha_a_pagar = fecha_pago)
            if i <= instance.periodo_reajuste:
                valor_arriendo = instance.valor_arriendo
                detalle_arriendo.monto_a_pagar = valor_arriendo
            
            if i % instance.periodo_reajuste == 1 and i != 1:
                detalle_arriendo.toca_reajuste = True   
            
            fechas_pago.append(detalle_arriendo)
            
        DetalleArriendo.objects.bulk_create(fechas_pago)

        instance.save(update_fields=["estado_arriendo", "comision", "valor_arriendo"])
        

@receiver(post_save, sender=ValoresGlobales)
def _post_save_valores_globales(sender, instance, created, **kwargs):
    if not created and instance.id == ValoreGlobalEnum.IMPUESTO_HONORARIO:
        nuevo_impuesto_honorario = instance.valor
        
        arriendos = Arriendo.objects.all().filter(estado_arriendo = True)

        for arriendo in arriendos:
            pctje_cobro_honorario = arriendo.propiedad.propietario.pctje_cobro_honorario
            nueva_comision = (pctje_cobro_honorario * (nuevo_impuesto_honorario / 100)) + pctje_cobro_honorario
            arriendo.comision = nueva_comision

            arriendo.valor_arriendo = (arriendo.valor_arriendo * (nueva_comision / 100)) + arriendo.valor_arriendo
            #modificar valor de detalle_arriendo


        Arriendo.objects.bulk_update(arriendos, ["comision", "valor_arriendo"])


@receiver(pre_save, sender=Propietario)
def _post_save_propietario(sender, instance, **kwargs):
    if instance.id:
        pctje_cobro_honorario_new = instance.pctje_cobro_honorario
        prop_old = Propietario.objects.get(pk=instance.id)
        pctje_cobro_honorario_old = prop_old.pctje_cobro_honorario
        impuesto_honorario = ValoresGlobales.objects.get(pk=ValoreGlobalEnum.IMPUESTO_HONORARIO)
        if pctje_cobro_honorario_new != pctje_cobro_honorario_old:

            nueva_comision = (pctje_cobro_honorario_new * (impuesto_honorario.valor / 100)) + pctje_cobro_honorario_new

            for propiedad in instance.propiedad_set.all():

                arriendos = propiedad.arriendo_set.all().filter(estado_arriendo=True)

                for arriendo in arriendos:
                    arriendos.comision = nueva_comision
                    arriendo.valor_arriendo = (propiedad.valor_arriendo_base * (nueva_comision / 100)) + propiedad.valor_arriendo_base
                    #modificar valor de detalle_arriendo
                    
                Arriendo.objects.bulk_update(arriendos, ["comision", "valor_arriendo"])

@receiver(pre_save, sender=ServiciosExtras)
def calcular_monto_cuotas(sender, instance, **kwargs):
    if instance.monto > 0 and instance.nro_cuotas > 0:
        instance.monto_cuotas = instance.monto / instance.nro_cuotas


@receiver(pre_save, sender=Propiedad)
def reajustar_valor_arriendo(sender, instance, **kwargs):
    try:
        propiedadOld = Propiedad.objects.get(pk=instance.id)
        propiedadNew = instance
        if propiedadNew.valor_arriendo_base != propiedadOld.valor_arriendo_base:
            arriendos = propiedadOld.arriendo_set.all().filter(estado_arriendo=True)
            for arriendo in arriendos:
                valor_arriendo = (propiedadNew.valor_arriendo_base * (arriendo.comision / 100)) + propiedadNew.valor_arriendo_base
                nueva_fecha_reajuste = datetime.utcnow() + relativedelta(months=arriendo.periodo_reajuste)

                arriendo.valor_arriendo = valor_arriendo
                arriendo.fecha_reajuste = nueva_fecha_reajuste
                #modificar valor de detalle_arriendo


            Arriendo.objects.bulk_update(arriendos, ["valor_arriendo", "fecha_reajuste"])
    except:
       pass


@receiver(post_save, sender=Propiedad)
def asignar_codigo_propiedad(sender, instance, created, **kwargs):
    if created:
        codigoPropiedad = CodigoPropiedad.objects.get(cod=instance.cod)
        codigoPropiedad.propiedad = instance
        codigoPropiedad.save(update_fields=['propiedad'])
