from django.contrib import admin
from .models import Client, Project, Quotation, DeliveryOrder, PurchaseOrder, Invoice, Payment

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Quotation)
admin.site.register(DeliveryOrder)
admin.site.register(PurchaseOrder)
admin.site.register(Invoice)
admin.site.register(Payment)
