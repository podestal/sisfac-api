from django.db import models
from django.conf import settings


class Baja(models.Model):
    fecha_baja = models.DateField(null=False)
    fecha_emision = models.DateField(null=False)
    lote = models.IntegerField(null=False)
    cantidad = models.IntegerField(null=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False)
    ticket_sunat = models.CharField(max_length=100, null=False)
    denominacion = models.CharField(max_length=100, null=False)
    digest_value = models.TextField(null=False)
    signature_value = models.TextField(null=False)
    enviada_sunat = models.BooleanField(default=False, null=False)
    aceptada_sunat = models.BooleanField(default=False, null=False)


class Comprobante(models.Model):
    codigo = models.CharField(max_length=10, null=False)
    descripcion = models.CharField(max_length=100, null=False)
    creado = models.DateTimeField(null=False)
    actualizado = models.DateTimeField(null=False)


# class Recibo(models.Model):
#     fecha_emision = models.DateField(null=False)
#     fecha_vencimiento = models.DateField(null=False)
#     comprobante = models.ForeignKey(Comprobante, on_delete=models.CASCADE, null=False)
#     serie = models.CharField(max_length=10, null=False)
#     numero = models.IntegerField(null=False)
#     exportacion = models.BooleanField(default=False, null=False)
#     moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=False)
#     gravada = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
#     inafecta = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
#     exonerada = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
#     igv = models.DecimalField(max_digits=10, decimal_places=2, null=False)
#     descuento = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
#     igv_porcentaje = models.DecimalField(max_digits=10, decimal_places=2, null=False)
#     detraccion = models.BooleanField(default=False, null=False)
#     observaciones = models.CharField(max_length=255, null=False)
#     digest_value = models.TextField(null=False)
#     signature_value = models.TextField(null=False)
#     enviada_sunat = models.BooleanField(default=False, null=False)
#     aceptada_sunat = models.BooleanField(default=False, null=False)
#     usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
#     negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, null=False)
#     persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=False)
#     direccion = models.CharField(max_length=200, null=False)
#     consulta_ticket = models.CharField(max_length=100, null=False)
#     motivo_baja = models.CharField(max_length=1000, null=False)
#     fecha_baja = models.DateField(null=False)
#     fecha_resumen = models.DateField(null=False)
#     anulada = models.BooleanField(default=False, null=False)
#     resumen = models.ForeignKey(Resumen, on_delete=models.CASCADE, null=False)
#     tipo_recibo_modificado = models.ForeignKey(Tipo_Recibo_Modificado, on_delete=models.CASCADE, null=False)
#     tipo_nota_credito = models.ForeignKey(Tipo_Nota_Credito, on_delete=models.CASCADE, null=False)
#     tipo_nota_debito = models.ForeignKey(Tipo_Nota_Debito, on_delete=models.CASCADE, null=False)
#     motivo_modificacion = models.CharField(max_length=100, null=False)
#     serie_documento_modificado = models.CharField(max_length=60, null=False)
#     numero_documento_modificado = models.CharField(max_length=60, null=False)
#     baja = models.ForeignKey(Baja, on_delete=models.CASCADE, null=False)
#     observaciones_sunat = models.CharField(max_length=2000, null=False)
#     codigo_error = models.CharField(max_length=60, null=False)
#     error_sunat = models.CharField(max_length=2000, null=False)
#     numero_parte = models.IntegerField(null=False)
#     agrupado = models.IntegerField(null=False)


class Item_Recibo(models.Model):
    cantidad = models.DecimalField(max_digits=10, decimal_places=1, null=False)
    descripcion = models.CharField(max_length=200, null=False)
    valor_unitario = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        null=False,
        default=0)
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    igv = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    # recibo = models.ForeignKey(Recibo, on_delete=models.CASCADE, null=False)
    # catalogo = models.ForeignKey(Catalogo, on_delete=models.CASCADE, null=False)
    # tipo_igv = models.ForeignKey(Tipo_IGV, on_delete=models.CASCADE, null=False)