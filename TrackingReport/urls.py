from django.contrib import admin
from django.urls import path
from app import views as appViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appViews.home, name='home'),
    
    path('client/', appViews.client, name='client'),
    path('client/add/', appViews.addClient, name='addClient'),
    path('client/view/<int:clientId>', appViews.viewClient, name='viewClient'),
    path('client/edit/<int:clientId>', appViews.editClient, name='editClient'),
    path('client/delete/<int:clientId>', appViews.deleteClient, name='deleteClient'),
    path('client/report/<int:clientId>', appViews.viewClientReport, name='viewClientReport'),

    path('project/', appViews.project, name='project'),
    path('project/add', appViews.addProject, name='addProject'),
    path('project/view/<int:projectId>', appViews.viewProject, name='viewProject'),
    path('project/edit/<int:projectId>', appViews.editProject, name='editProject'),
    path('project/delete/<int:projectId>', appViews.deleteProject, name='deleteProject'),
    path('project/report/<int:projectId>', appViews.viewProjectReport, name='viewProjectReport'),

    path('quotation/add/<int:projectId>', appViews.addQuotation, name='addQuotation'),
    path('quotation/view/<int:quotationId>', appViews.viewQuotation, name='viewQuotation'),
    path('quotation/edit/<int:quotationId>', appViews.editQuotation, name='editQuotation'),
    path('quotation/delete/<int:quotationId>', appViews.deleteQuotation, name='deleteQuotation'),
    path('quotation/editPrint/<int:projectId>', appViews.editPrintStatus, name='editPrintStatus'),
    path('quotation/savePrint/', appViews.savePrintStatus, name='savePrintStatus'),

    path('deliveryOrder/add/<int:quotationId>', appViews.addDeliveryOrder, name='addDeliveryOrder'),
    path('deliveryOrder/edit/<int:deliveryId>', appViews.editDeliveryOrder, name='editDeliveryOrder'),
    path('deliveryOrder/delete/<int:deliveryId>', appViews.deleteDeliveryOrder, name='deleteDeliveryOrder'),

    path('purchaseOrder/add/<int:quotationId>', appViews.addPurchaseOrder, name='addPurchaseOrder'),
    path('purchaseOrder/edit/<int:purchaseId>', appViews.editPurchaseOrder, name='editPurchaseOrder'),
    path('purchaseOrder/delete/<int:purchaseId>', appViews.deletePurchaseOrder, name='deletePurchaseOrder'),

    path('invoice/add/<int:quotationId>', appViews.addInvoice, name='addInvoice'),
    path('invoice/view/<int:invoiceId>', appViews.viewInvoice, name='viewInvoice'),
    path('invoice/edit/<int:invoiceId>', appViews.editInvoice, name='editInvoice'),
    path('invoice/delete/<int:invoiceId>', appViews.deleteInvoice, name='deleteInvoice'),

    path('payment/add/<int:invoiceId>', appViews.addPayment, name='addPayment'),
    path('payment/edit/<int:paymentId>', appViews.editPayment, name='editPayment'),
    path('payment/delete/<int:paymentId>', appViews.deletePayment, name='deletePayment'),
]
