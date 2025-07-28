from urllib.request import Request

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import ModelForm, OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders_delivered = orders.filter(status = 'Delivered').count()
    total_orders_pending = orders.filter(status = 'Pending').count()
    total_orders = orders.count()
    context = {'orders': orders, 'customers': customers, 'total_customer': total_customer, 'total_orders_delivered' : total_orders_delivered, 'total_orders_pending': total_orders_pending , 'total_orders': total_orders}
    return render (request, 'account/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render (request, 'account/products.html', {'products': products})


def customer(request, id):
    cust = Customer.objects.get(id = id)
    orders = cust.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'cust': cust, 'orders': orders, 'order_count' : order_count, 'myFilter' : myFilter}
    return render (request, 'account/customer.html', context)


def view_customer_list(request):
    customer_list = Customer.objects.all().order_by('date_created')
    paginator = Paginator(customer_list, 10)

    page_number = request.GET.get('page')  # Get the current page number from the request
    customers = paginator.get_page(page_number)  # Returns a Page object

    return render(request, 'account/view_customers_list.html', {'customers': customers})

def createOrder(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id = id)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # print('Printing POST: ', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
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
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'account/delete_form.html', context)







def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form' : form}
    return render(request, 'account/register.html', context)



def loginPage(request):
    context = {}
    return render(request, 'account/login.html', context)

