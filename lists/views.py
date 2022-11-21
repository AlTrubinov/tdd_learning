from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    '''Домашняя страница'''
    return render(request, 'home.html')

def new_list(request):
    '''Новый список'''
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/one-lists/')

def view_list(request):
    '''Представление списка'''
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
