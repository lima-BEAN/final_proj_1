from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
#TODO: Require login to create App in LimaBeanLab Apps section
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.decorators import login_required

from .forms import KitchenForm, NewCustomerForm, CartAddItemForm, OrderCreateForm
from .models import Kitchen, Food, Customer, Order, OrderItem
from .cart import Cart


# def home(request):
#     return HttpResponse("It works")
class home(ListView):
    template_name = 'kitchen/home.html'
    model = Kitchen
    context_object_name = 'kitchens'

class KitchenDetailView(DetailView):
    model = Kitchen
    template_name = 'kitchen/kitchen_detail.html'
    context_object_name = 'kitchen'
    food = Food.objects.all()
    customers = Customer.objects.all()

    extra_context = {'cart_add_form': CartAddItemForm(), 'foods': food, 'customers':customers}


class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'registration/new_customer.html'
    success_url = reverse_lazy('kitchen:home')
    login_url = '/login/'

    def new_customer(request):
        if request.method == 'POST':
            f = NewCustomerForm(request.POST)
            if f.is_valid():
                f.save()
                messages.success(request, 'Account created successfully')
                return HttpResponseRedirect(reverse_lazy('kitchen:login'))
            else:
                return HttpResponse('Form not valid')
        else:
            f = NewCustomerForm()
        return render(request, 'registration/new_customer.html', {'form': f})

class CustomerListView(ListView):
    model = Customer
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['customers'] = Customer.objects.all()
        context['customer_list'] = Customer.objects.all()
        context['kitchen_list'] = Kitchen.objects.all()
        context['order_list'] = Order.objects.all()
        return context


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['username', 'email', 'password']
    template_name = 'customer/customer_update.html'
    success_url = reverse_lazy('kitchen:customer_detail')
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # context['customers'] = Customer.objects.all()
        context['customer_list'] = Customer.objects.all()

        return context

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('kitchen:home')

class ProviderKitchenListView(LoginRequiredMixin,ListView):
    model = Kitchen
    context_object_name = 'kitchen'
    template_name = 'kitchen/kitchen_list.html'
    def get_queryset(self):
        user = self.request.user
        customer = get_object_or_404(Customer,username=user)
        return Kitchen.objects.filter(customer=customer)

def ProviderKitchenDetailView(request, pk):
    kitchen_obj = get_object_or_404(Kitchen, pk=pk)
    FoodFormSet = inlineformset_factory(Kitchen, Food, fields='__all__',extra=1, max_num=10)
    Form = FoodFormSet(instance=kitchen_obj)
    if request.method == 'POST':
        form = FoodFormSet(request.POST, instance=kitchen_obj)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'kitchen/provider_kitchen_detail.html',{'kitchen': kitchen_obj, 'form': Form,'error': 'Bad data entry'})
        return redirect('kitchen:provider_kitchen_detail', pk=kitchen_obj.id)
    return render(request, 'kitchen/provider_kitchen_detail.html',{'kitchen': kitchen_obj, 'form': Form})

@login_required(login_url='kitchen:login')
def KitchenCreateView(request):
    customer = get_object_or_404(Customer, username=request.user)
    form = KitchenForm()
    # FoodFormSet = inlineformset_factory(Kitchen, Food, fields=('name','diet','price'),extra=5, max_num=5)
    if request.method == 'POST':
        form = KitchenForm(request.POST, request.FILES)
        if form.is_valid():
            k_instance = Kitchen.objects.create(
                name=form.cleaned_data.get('name'),
                open_time=form.cleaned_data.get('open_time'),
                close_time=form.cleaned_data.get('close_time'),
                image=form.cleaned_data.get('image'),
                working_days=form.cleaned_data.get('working_days'),
                customer=customer
            )
            k_instance.save()
        else:
            return render(request, 'kitchen/kitchen_create.html',{'kitchen_form':form,'error': 'Bad data entry'})
        return HttpResponseRedirect(reverse_lazy('kitchen:provider_kitchen_detail',args=(k_instance.id,)))
    if not customer.is_provider:
        customer.is_provider = True
        customer.save()
    return render(request, 'kitchen/kitchen_create.html',{'kitchen_form':form})

class KitchenUpdateView(UpdateView):
    model = Kitchen
    fields = ['name',  'open_time', 'close_time', 'working_days']
    template_name = 'kitchen/kitchen_update.html'
    success_url = reverse_lazy('kitchen:index')
    #TODO # login_url = '/login/'

class KitchenDeleteView(DeleteView):
    model = Kitchen
    template_name = 'kitchen/kitchen_confirm_delete.html'
    success_url = reverse_lazy('kitchen:index')
    #TODO: # login_url = '/login/'


def profile(request):
    # return HttpResponse('this is the profile page')
    return render (request, 'accounts/profile.html')


def register(request):
    if request.method == 'POST':
        f = NewCustomerForm(request.POST)
        print('is the CUSTOMERFORM WORKING: {}'.format(f))
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect(reverse_lazy('kitchen:login'))
        else:
            return HttpResponse('Form not valid')
    else:
        f = NewCustomerForm()
    return render(request, 'registration/register.html', {'form': f})

@require_POST
def CartAdd(request, pk):
    cart = Cart(request)
    food = get_object_or_404(Food, id=pk)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=food,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('kitchen:cart_detail')


def CartRemove(request, pk):
    cart = Cart(request)
    item = get_object_or_404(Food, id=pk)
    cart.remove(item)
    return redirect('kitchen:cart_detail')


def CartDetail(request):
    cart = Cart(request)
    kitchen_id = ''
    for item in cart:
        item['update_quantity_form'] = CartAddItemForm(initial={'quantity': item['quantity'],'update': True})
        kitchen_id = item['item'].kitchen_id
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'kitchen_id': kitchen_id})



def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            customer = get_object_or_404(Customer, username=request.user)
            order.customer = customer
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         food=item['item'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                # kitchen_id = item['item'].kitchen.id
            # clear the cart
            cart.clear()
            # launch asynchronous task
            # send success email
            # order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect to the payment
            return redirect(reverse('kitchen:order_success'))
    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'cart': cart,
                                                        'form': form})

def OrderSuccess(request):
    # send email
    return render(request, 'order/order_success.html')

def check():
    pass

def error_500(request):
    return render(request, '500.html')
