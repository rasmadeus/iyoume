from django.contrib import admin
from iyoume.waybill import models


class WaybillAdmin(admin.ModelAdmin):
    list_display = ('user')


admin.site.register(models.Waybill)
admin.site.register(models.GeoPoint)
admin.site.register(models.Passenger)
admin.site.register(models.Travel)