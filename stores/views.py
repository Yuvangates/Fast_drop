from django.shortcuts import render,redirect
from .models import Store,Item
from .forms import ItemForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from . import forms
# Create your views here.
def stores_list(request):
    # return('uvan') 
    stores = Store.objects.all().order_by('created_at')
    return render(request,'stores/stores_list.html',{'stores':stores})

def items_list(request):
    """ New view to display all items from all stores """
    items = Item.objects.all()
    return render(request, 'stores/items_list.html', {'items': items})

# def store_details(request,slug):
#     # return HttpResponse(slug)
#     store = Store.objects.get(slug=slug)
#     return render(request,'stores/stores_detail.html',{'store':store})
# @login_required(login_url="/accounts/login/")
# def store_create(request):
#     if request.method == 'POST':
#         form=forms.CreateStore(request.POST,request.FILES)
#         if form.is_valid():
#             #save to database
#             instance = form.save(commit=False)
#             instance.author = request.user
#             instance.save()
#             return redirect('stores:list')
#     else:
#         form = forms.CreateStore()
#     return render(request,'stores/store_create.html',{'form':form})
@login_required
def add_item(request):
    # Check if user is a store manager
    if request.user.is_staff and hasattr(request.user, 'store'):
        store = request.user.store
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.store = store
                item.save()
                return redirect('stores:manager_dashboard')
        else:
            form = ItemForm()
        return render(request, 'stores/add_item.html', {'form': form})
    else:
        return render(request, 'stores/no_access.html')

@login_required
def manager_dashboard(request):
    if request.user.is_staff and hasattr(request.user, 'store'):
        store = request.user.store
        items = store.items.all()
        return render(request, 'stores/manager_dashboard.html', {'store': store, 'items': items})
    else:
        return render(request, 'stores/no_access.html')
