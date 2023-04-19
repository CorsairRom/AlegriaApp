from django.contrib import admin
from ApiArriendosAlegria.models import Usuario, Banco, TipoCuenta, TipoTrabajador

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Banco)
admin.site.register(TipoCuenta)
admin.site.register(TipoTrabajador)

