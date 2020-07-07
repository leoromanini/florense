from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Environment)
admin.site.register(Order)
admin.site.register(Label)
admin.site.register(Product)
admin.site.register(Room)
admin.site.register(ProductBelongs)
admin.site.register(LabelBelongs)
admin.site.register(Allocation)
admin.site.register(RoomLabel)
