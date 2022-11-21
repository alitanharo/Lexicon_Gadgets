from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from lexiconapp.models import *
from lexiconapp import forms
from django.contrib.auth.forms import UserChangeForm
from .models import ProfileUpdateForm,UserUpdateForm,Customer,OrderItem,Order
from django.urls import reverse
from django.template import loader
from django.utils import timezone

# Create your views here.

def check_admin(user):
    # print(user.is_superuser)
    return user.is_superuser

def error_404_view(request, exception):
    return redirect('userlogin')

def index(request):
    return render(request, 'lexiconapp/base.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:

            messages.error(
                request, "Password does not Match,Please Try Again!")
            return redirect('/signup')
        try:
            if User.objects.get(username=username):
                messages.warning(request, "Username Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass
        # checks for error inputs
        user = User.objects.create_user(username, email, pass1)
        user.save()
        customer = Customer(user=user,name=username,email=email)
        customer.save()
        messages.info(request, 'Thanks For Signing Up')
        # messages.info(request,"Signup Successful Please Login")
        return redirect('/login')
    return render(request, "lexiconapp/signup.html")


def userlogin(request):

    if request.method == 'POST':
        login_form = forms.UserLogin(data=request.POST)

        myusername = request.POST['username']
        mypassword = request.POST['password']

        user = authenticate(username=myusername, password=mypassword)
        print(user)
        # user = not None
        if user is not None:
            login(request, user)
            return render(request, 'lexiconapp/login.html', {'user': user})
        else:
            print("error")

    else:
        login_form = forms.UserLogin()

    return render(request, 'lexiconapp/login.html', {'login_form': login_form})

@login_required
def orderconf(request):
    # need to take orderno from order model
    customer = Customer.objects.get(name=request.user)
    orderno = Order.objects.get(customer=customer)
    t_id=orderno.transaction_id
    return HttpResponse("Your order is placed. order no {}".format(t_id))

@login_required
def orderbyuser(request):
    customer = Customer.objects.get(name=request.user)
    orders = Order.objects.filter(customer=customer)
    orderitems = OrderItem.objects.filter(order__in=orders)
    shippingaddress = ShippingAddress.objects.filter(order__in=orders)

    
    context = {
    'orders': orders,
    'orderitems' : orderitems,
    'shippingaddress' : shippingaddress,
    }    
    return render(request, 'lexiconapp/orders.html', context)



@login_required
def userlogout(request):
    logout(request)
    messages.success(request, 'logged out success')
    return redirect('userlogin')


def card(request):
    item_list = Product.objects.all().values()
    context = {'items': item_list, }
    return render(request, 'lexiconapp/card.html', context)

def add(request):
    template = loader.get_template('lexiconapp/add.html')
    return HttpResponse(template.render({}, request))

@user_passes_test(check_admin)
def addrecord(request):
    a = request.POST.get('Title', False)
    d = request.POST.get('Description', False)
    e = request.POST.get('Price', False)
    b = request.POST.get('Brand', False)
    f = request.POST.get('Category', False)
    c = request.POST.get('Images', False)
    product = Product(title=a, description=d, price=e,
                      brand=b, category=f, images=c)
    product.save()
    return HttpResponseRedirect(reverse('card'))

# update record
def updaterecord(request, id):
    a = request.POST.get('Title', False)
    d = request.POST.get('Description', False)
    e = request.POST.get('Price', False)
    b = request.POST.get('Brand', False)
    f = request.POST.get('Category', False)
    c = request.POST.get('Images', False)
    product = Product.objects.get(id=id)
    product.title = a
    product.description = d
    product.price = e
    product.brand = b
    product.category = f
    product.images = c
    product.save()
    return HttpResponseRedirect(reverse('card'))

def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponseRedirect(reverse('card'))

def update(request, id):
    selected_product = Product.objects.get(id=id)
    template = loader.get_template('lexiconapp/update.html')
    context = {
        'item': selected_product,
    }
    return HttpResponse(template.render(context, request))


def contact(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # if len(name) > 4 and len(phone) > 8 and len(message) > 2:
        #     messages.error(request, "Please fill the form correctly")
        # else:
        contact.name = name
        contact.email = email
        contact.phone = phone
        contact.message = message
        contact.save()
        messages.success(request, "Your message has been successfully sent")
    return render(request, 'lexiconapp/contact.html')


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')  # Redirect back to profile page

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'lexiconapp/profile.html', context)


@login_required(login_url='login')
def updateprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'lexiconapp/updateprofile.html', context)



def add_to_basket(request,title):
    item= get_object_or_404(Product,title=title)
    order_item = OrderItem.objects.create(product = item)
    order_qs = Order.objects.filter(customer= request.customer,  complete = False)
    if order_qs.exists():
        order=order_qs[0]
        
        if order.items.filter(item__title = item.title).exists():
            order_item.quantity +=1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        date_ordered=timezone.now()
        order= Order.objects.create(customer = request.customer, date_ordered=date_ordered)
        order.items.add(order_item)
        return redirect("card",title=title)





    # Redirect back to profile page
