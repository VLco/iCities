from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(City)
admin.site.register(Region)
admin.site.register(Indicator)
admin.site.register(TypeCity)
admin.site.register(CategoryIdicators)


class ListIndicatorsAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'city')
    list_filter = ('indicator', 'date')
    pass


admin.site.register(ListIndicators, ListIndicatorsAdmin)
