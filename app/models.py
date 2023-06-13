from django.db import models
from django.db.models import Sum

class Client(models.Model):
    clientName = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phoneNo = models.CharField(max_length=15, null=True, blank=True)
    status = models.BooleanField(default=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)

class Project(models.Model):
    projectName = models.CharField(max_length=500, null=True, blank=True)
    status = models.BooleanField(default=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, blank=True, related_name='projects')

    @property
    def numOfQuo(self):
        return self.quotation.count()
    
    @property
    def totalQuotation(self):
        amount = 0
        for quotation in self.quotation.all():
            amount += quotation.amount
        return amount
    
    @property
    def totalInvoice(self):
        amount = 0
        if self.quotation.exists():
            for quotation in self.quotation.all():
                if quotation.invoice.exists():
                    for invoice in quotation.invoice.all():
                        amount += invoice.amount
        return amount
    
    @property
    def totalPaid(self):
        amount = 0
        if self.quotation.exists():
            for quotation in self.quotation.all():
                if quotation.invoice.exists():
                    for invoice in quotation.invoice.all():
                        if invoice.payment.exists():
                            for payment in invoice.payment.all():
                                amount += payment.amount
        return amount
    
    @property
    def totalBalance(self):
        amount = 0
        if self.quotation.exists():
            for quotation in self.quotation.all():
                if quotation.invoice.exists():
                    for invoice in quotation.invoice.all():
                        if invoice.payment.exists():
                            amount += invoice.payment.last().balance
                        else:
                            amount += invoice.amount
        return amount if amount is not 0 else self.totalInvoice

class Quotation(models.Model):
    date = models.DateField(null=True, blank=True)
    quotationNo = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    emailDate = models.DateField(null=True, blank=True)
    printStatus = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True, related_name='quotation')

    @property
    def totalInvoice(self):
        return self.invoice.aggregate(total=Sum('amount')).get('total') or 0
    
    @property
    def paidAmount(self):
        return self.invoice.aggregate(total=Sum('payment__amount')).get('total') or 0
    
    @property
    def totalBalance(self):
        balance = 0
        for invoice in self.invoice.all():
            if invoice.payment.exists():
                balance += invoice.payment.last().balance
            else:
                balance += invoice.amount
        return balance if balance is not 0 else self.totalInvoice
    
    # @property
    # def totalBalance(self):
    #     total_balance = sum(invoice.payment.last().balance for invoice in self.invoice.all() if invoice.payment.exists())
    #     return total_balance if total_balance is not None else 0
    
class DeliveryOrder(models.Model):
    date = models.DateField(null=True, blank=True)
    doNo = models.CharField(max_length=50, null=True, blank=True)
    emailDate = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)
    quotation = models.ForeignKey('Quotation', on_delete=models.CASCADE, null=True, blank=True, related_name='delivery')

class PurchaseOrder(models.Model):
    date = models.DateField(null=True, blank=True)
    poNo = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)
    quotation = models.ForeignKey('Quotation', on_delete=models.CASCADE, null=True, blank=True, related_name='purchase')

class Invoice(models.Model):
    date = models.DateField(null=True, blank=True)
    invNo = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    emailDate = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)
    quotation = models.ForeignKey('Quotation', on_delete=models.CASCADE, null=True, blank=True, related_name='invoice')

class Payment(models.Model):
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    createdOn = models.DateTimeField(null=True, blank=True)
    updatedOn = models.DateTimeField(null=True, blank=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, blank=True, related_name='payment')

    @property
    def balance(self):
        prevPayment = Payment.objects.filter(invoice=self.invoice, status=True, date__lt=self.date)
        prevBalance = sum([p.amount for p in prevPayment])
        return self.invoice.amount - prevBalance - self.amount
