from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import ModelForm, OrderForm


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders_delivered = orders.filter(status = 'Delivered').count()
    total_orders_pending = orders.filter(status = 'Pending').count()
    total_orders = orders.count()
    context = {'orders': orders, 'customers': customers, 'total_customer' : total_customer, 'total_orders_delivered' : total_orders_delivered, 'total_orders_pending': total_orders_pending , 'total_orders': total_orders}
    return render (request, 'account/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render (request, 'account/products.html', {'products': products})


def customer(request, id):
    cust = Customer.objects.get(id = id)
    # customers = Customer.objects.all()
    orders = cust.order_set.all()
    context = {'cust': cust, 'orders': orders}
    return render (request, 'account/customer.html', context)


def view_customer_list(request):
    customer_list = Customer.objects.all().order_by('date_created')
    paginator = Paginator(customer_list, 10)

    page_number = request.GET.get('page')  # Get the current page number from the request
    customers = paginator.get_page(page_number)  # Returns a Page object

    return render(request, 'account/view_customers_list.html', {'customers': customers})

def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST: ', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'account/order_form.html', context)

def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        # print('Printing POST: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'account/update_form.html', context)

def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm()

    context = {'form': form}
    return render(request, 'account/delete_form.html', context)

