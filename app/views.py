from django.shortcuts import render, redirect
from .models import Client, Project, Quotation, DeliveryOrder, PurchaseOrder, Invoice, Payment
from datetime import datetime
from django.http import JsonResponse
import json
from django.db.models import Sum

def home(request):
    # company summary
    projectCount = Project.objects.all().count()
    invoiceSum = 0
    paidSum = 0
    balanceSum = 0
    projects = Project.objects.all()
    for project in projects:
        invoiceSum += project.totalInvoice
        paidSum += project.totalPaid
        balanceSum += project.totalBalance

    clients = Client.objects.all()
    return render(request, 'app/home.html', {'clients':clients, 'projectCount':projectCount, 'invoiceSum':invoiceSum, 'paidSum':paidSum, 'balanceSum':balanceSum})

def client(request):
    clients = Client.objects.filter(status=True)
    return render(request, 'app/client.html', {'clients':clients})

def addClient(request):
    if request.method == 'POST':
        clientName = request.POST.get('clientName')
        phoneNo = request.POST.get('phoneNo')
        email = request.POST.get('email')

        client = Client(
            clientName = clientName,
            phoneNo = phoneNo,
            email = email,
            createdOn = datetime.now()
        )
        client.save()
        return redirect('client')
    else:
        return render(request, 'app/add-client.html', {})
    
def viewClient(request, clientId):
    client = Client.objects.get(id=clientId)
    projects = client.projects.all()
    return render(request, 'app/view-client.html', {'client':client, 'projects':projects})

def editClient(request, clientId):
    client = Client.objects.get(id=clientId)
    if request.method == 'POST':
        clientName = request.POST.get('clientName')
        phoneNo = request.POST.get('phoneNo')
        email = request.POST.get('email')
        
        client.clientName = clientName
        client.phoneNo = phoneNo
        client.email = email
        client.updatedOn = datetime.now()
        client.save()
        return redirect('viewClient', client.id)
    else:
        return render(request, 'app/edit-client.html', {'client':client})
    
def deleteClient(request, clientId):
    Client.objects.filter(id=clientId).delete()
    return redirect('client')

def project(request):
    projects = Project.objects.filter(status=True)
    return render(request, 'app/project.html', {'projects':projects})

def addProject(request):
    clients = Client.objects.filter(status=True)

    if request.method == 'POST':
        projectName = request.POST.get('projectName')
        clientId = request.POST.get('clientId')

        project = Project(
            projectName = projectName,
            createdOn = datetime.now()
        )
        if clientId != '':
            client = Client.objects.get(id=clientId)
            project.client = client
        project.save()

        return redirect('viewProject', project.id)
    else:
        return render(request, 'app/add-project.html', {'clients':clients})

def viewProject(request, projectId):
    project = Project.objects.get(id=projectId)
    quotations = project.quotation.filter(status=True).order_by('date')
    return render(request, 'app/view-project.html', {'project':project, 'quotations':quotations})

def editProject(request, projectId):
    project = Project.objects.get(id=projectId)
    clients = Client.objects.filter(status=True)
    
    if request.method == 'POST':
        projectName = request.POST.get('projectName')
        clientId = request.POST.get('clientId')

        project.projectName = projectName
        client = Client.objects.get(id=clientId)
        project.client = client
        project.updatedOn = datetime.now()
        project.save()
        return redirect('viewProject', project.id)
    else:
        return render(request, 'app/edit-project.html', {'project':project, 'clients':clients})
    
def deleteProject(request, projectId):
    Project.objects.filter(id=projectId).delete()
    return redirect('project')

def addQuotation(request, projectId):
    project = Project.objects.get(id=projectId)

    if request.method == 'POST':
        date = request.POST.get('date')
        quotationNo = request.POST.get('quotationNo')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        emailDate = request.POST.get('emailDate')

        quotation = Quotation(
            quotationNo = quotationNo,
            description = description,
            amount = amount,
            createdOn = datetime.now(),
            project = project
        )
        if date != '':
            quotation.date = date
        if emailDate != '':
            quotation.emailDate = emailDate
        quotation.save()
        return redirect('viewProject', project.id)
    else:
        return render(request, 'app/add-quotation.html', {'project':project})
    
def viewQuotation(request, quotationId):
    context = {}
    quotation = Quotation.objects.get(id=quotationId)
    context['quotation'] = quotation

    delivery = quotation.delivery.filter(status=True)
    if delivery != None:
        context['delivery'] = delivery

    purchase = quotation.purchase.filter(status=True)
    if purchase != None:
        context['purchase'] = purchase

    invoices = quotation.invoice.filter(status=True).order_by('date')
    if invoices != None:
        context['invoices'] = invoices

    return render(request, 'app/view-quotation.html', context)

def editQuotation(request, quotationId):
    quotation = Quotation.objects.get(id=quotationId)

    if request.method == 'POST':
        date = request.POST.get('date')
        quotationNo = request.POST.get('quotationNo')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        emailDate = request.POST.get('emailDate')

        if date != '':
            quotation.date = date
        quotation.quotationNo = quotationNo
        quotation.description = description
        quotation.amount = amount
        if emailDate != '':
            quotation.emailDate = emailDate
        quotation.updatedOn = datetime.now()
        quotation.save()
        
        return redirect('viewQuotation', quotation.id)
    else:
        return render(request, 'app/edit-quotation.html', {'quotation':quotation})
    
def deleteQuotation(request, quotationId):
    quotation = Quotation.objects.get(id=quotationId)
    projectId = quotation.project.id
    quotation.delete()
    return redirect('viewProject', projectId)

def addDeliveryOrder(request, quotationId):
    quotation = Quotation.objects.get(id=quotationId)

    if request.method == 'POST':
        date = request.POST.get('date')
        doNo = request.POST.get('doNo')
        emailDate = request.POST.get('emailDate')

        delivery = DeliveryOrder(
            doNo = doNo,
            createdOn = datetime.now(),
            quotation = quotation
        )
        if date != '':
            delivery.date = date
        if emailDate != '':
            delivery.emailDate = emailDate
        delivery.save()
        return redirect('viewQuotation', quotation.id)
    else:
        return render(request, 'app/add-delivery-order.html', {'quotation':quotation})
    
def editDeliveryOrder(request, deliveryId):
    delivery = DeliveryOrder.objects.get(id=deliveryId)

    if request.method == 'POST':
        date = request.POST.get('date')
        doNo = request.POST.get('doNo')
        emailDate = request.POST.get('emailDate')

        if date != '':
            delivery.date = date
        delivery.doNo = doNo
        if emailDate != '':
            delivery.emailDate = emailDate
        delivery.updatedOn = datetime.now()
        delivery.save()
        return redirect('viewQuotation', delivery.quotation.id)
    else:
        return render(request, 'app/edit-delivery-order.html', {'delivery':delivery})
    
def deleteDeliveryOrder(request, deliveryId):
    delivery = DeliveryOrder.objects.get(id=deliveryId)
    quotationId = delivery.quotation.id
    delivery.delete()
    return redirect('viewQuotation', quotationId)

def addPurchaseOrder(request, quotationId):
    quotation = Quotation.objects.get(id=quotationId)

    if request.method == 'POST':
        date = request.POST.get('date')
        poNo = request.POST.get('poNo')
        
        purchase = PurchaseOrder(
            date = date,
            poNo = poNo,
            createdOn = datetime.now(),
            quotation = quotation
        )
        if date != '':
            purchase.date = date
        purchase.save()
        return redirect('viewQuotation', quotation.id)
    else:
        return render(request, 'app/add-purchase-order.html', {'quotation':quotation})
    
def editPurchaseOrder(request, purchaseId):
    purchase = PurchaseOrder.objects.get(id=purchaseId)

    if request.method == 'POST':
        date = request.POST.get('date')
        poNo = request.POST.get('poNo')

        if date != '':
            purchase.date = date
        purchase.poNo = poNo
        purchase.updatedOn = datetime.now()
        purchase.save()
        return redirect('viewQuotation', purchase.quotation.id)
    else:
        return render(request, 'app/edit-purchase-order.html', {'purchase':purchase})
    
def deletePurchaseOrder(request, purchaseId):
    purchase = PurchaseOrder.objects.get(id=purchaseId)
    quotationId = purchase.quotation.id
    purchase.delete()
    return redirect('viewQuotation', quotationId)

def addInvoice(request, quotationId):
    quotation = Quotation.objects.get(id=quotationId)

    if request.method == 'POST':
        date = request.POST.get('date')
        invNo = request.POST.get('invNo')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        emailDate = request.POST.get('emailDate')

        invoice = Invoice(
            invNo = invNo,
            description = description,
            amount = amount,
            createdOn = datetime.now(),
            quotation = quotation
        )
        if date != '':
            invoice.date = date
        if emailDate != '':
            invoice.emailDate = emailDate
        invoice.save()
        return redirect('viewQuotation', quotation.id)
    else:
        return render(request, 'app/add-invoice.html', {'quotation':quotation})

def viewInvoice(request, invoiceId):
    invoice = Invoice.objects.get(id=invoiceId)
    payments = invoice.payment.filter(status=True).order_by('date')
    return render(request, 'app/view-invoice.html', {'invoice':invoice, 'payments':payments})

def editInvoice(request, invoiceId):
    invoice = Invoice.objects.get(id=invoiceId)

    if request.method == 'POST':
        date = request.POST.get('date')
        invNo = request.POST.get('invNo')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        emailDate = request.POST.get('emailDate')

        if date != '':
            invoice.date = date
        invoice.invNo = invNo
        invoice.description = description
        invoice.amount = amount
        if emailDate != '':
            invoice.emailDate = emailDate
        invoice.updatedOn = datetime.now()
        invoice.save()
        return redirect('viewInvoice', invoice.id)
    else:
        return render(request, 'app/edit-invoice.html', {'invoice':invoice})
    
def deleteInvoice(request, invoiceId):
    invoice = Invoice.objects.get(id=invoiceId)
    quotationId = invoice.quotation.id
    invoice.delete()
    return redirect('viewQuotation', quotationId)

def addPayment(request, invoiceId):
    invoice = Invoice.objects.get(id=invoiceId)

    if request.method == 'POST':
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        remark = request.POST.get('remark')

        payment = Payment(
            amount = amount,
            remark = remark,
            createdOn = datetime.now(),
            invoice = invoice
        )
        if date != '':
            payment.date = date
        payment.save()
        return redirect('viewInvoice', invoice.id)
    else:
        return render(request, 'app/add-payment.html', {'invoice':invoice})
    
def editPayment(request, paymentId):
    payment = Payment.objects.get(id=paymentId)

    if request.method == 'POST':
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        remark = request.POST.get('remark')

        if date != '':
            payment.date = date
        payment.amount = amount
        payment.remark = remark
        payment.updatedOn = datetime.now()
        payment.save()
        return redirect('viewInvoice', payment.invoice.id)
    else:
        return render(request, 'app/edit-payment.html', {'payment':payment})
    
def deletePayment(request, paymentId):
    payment = Payment.objects.get(id=paymentId)
    invoiceId = payment.invoice.id
    payment.delete()
    return redirect('viewInvoice', invoiceId)

def viewProjectReport(request, projectId):
    project = Project.objects.get(id=projectId)
    quotations = project.quotation.filter(status=True).order_by('date')

    # project summary total
    quotationSum = 0
    invoiceSum = 0
    paidSum = 0
    balanceSum = 0
    for quotation in quotations:
        quotationSum += quotation.amount
        invoiceSum += quotation.totalInvoice
        paidSum += quotation.paidAmount
        balanceSum += quotation.totalBalance

    return render(request, 'app/view-project-report.html', {'project':project, 'quotations':quotations, 'quotationSum':quotationSum, 'invoiceSum':invoiceSum, 'paidSum':paidSum, 'balanceSum':balanceSum})

def viewClientReport(request, clientId):
    client = Client.objects.get(id=clientId)
    projects = client.projects.filter(status=True)
    return render(request, 'app/view-client-report.html', {'client':client, 'projects':projects})

def editPrintStatus(request, projectId):
    project = Project.objects.get(id=projectId)
    quotations = project.quotation.all().order_by('date')
    return render(request, 'app/edit-print-status.html', {'project':project, 'quotations':quotations})

def savePrintStatus(request):
    if request.method == 'POST':
        print_data = json.loads(request.body.decode('utf-8'))

        # reset all quotation print status to false
        projectId = print_data['projectId']
        project = Project.objects.get(id=projectId)
        quotations = project.quotation.filter(status=True)
        for quotation in quotations:
            quotation.printStatus = False
            quotation.save()

        for qid in print_data['quotationId']:
            q = Quotation.objects.get(id=qid)
            q.printStatus = True
            q.save()

    return JsonResponse({'status':'success'})