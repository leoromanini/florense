from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Environment)
admin.site.register(Order)
admin.site.register(Label)
admin.site.register(Product)
admin.site.register(Room)
admin.site.register(ProductPermission)
admin.site.register(LabelPermission)
admin.site.register(AllocationProduct)
admin.site.register(AllocationLabel)
admin.site.register(AllocationRoom)
