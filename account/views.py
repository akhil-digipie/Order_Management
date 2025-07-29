from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import *
from .forms import ModelForm, OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, only_admin
from django.contrib.auth.models import Group

@login_required(login_url='login')
@only_admin
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders_delivered = orders.filter(status = 'Delivered').count()
    total_orders_pending = orders.filter(status = 'Pending').count()
    total_orders = orders.count()
    context = {'orders': orders, 'customers': customers, 'total_customer': total_customer, 'total_orders_delivered' : total_orders_delivered, 'total_orders_pending': total_orders_pending , 'total_orders': total_orders}
    return render (request, 'account/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render (request, 'account/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, id):
    cust = Customer.objects.get(id = id)
    orders = cust.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'cust': cust, 'orders': orders, 'order_count' : order_count, 'myFilter' : myFilter}
    return render (request, 'account/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def view_customer_list(request):
    customer_list = Customer.objects.all().order_by('date_created')
    paginator = Paginator(customer_list, 10)

    page_number = request.GET.get('page')  # Get the current page number from the request
    customers = paginator.get_page(page_number)  # Returns a Page object

    return render(request, 'account/view_customers_list.html', {'customers': customers})

@login_required(login_url='login')
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'account/delete_form.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customers')
            user.groups.add(group)
            Customer.objects.create(
                user = user,
            )



            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form' : form}
    return render(request, 'account/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid Credential')
    context = {}
    return render(request, 'account/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders_delivered = orders.filter(status='Delivered').count()
    total_orders_pending = orders.filter(status='Pending').count()
    total_orders = orders.count()

    print('orders' , orders)
    context = {'orders' : orders, 'total_orders_delivered' : total_orders_delivered, 'total_orders_pending' : total_orders_pending, 'total_orders': total_orders }
    return render(request, 'account/user_page.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customers'])
def accountSettings(request):
    context = {}
    return render(request, 'account/account_setting.html', context)



