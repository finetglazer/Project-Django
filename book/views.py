from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import logging
from django.shortcuts import render
from django.db.models import Q
from .models import Item


logger = logging.getLogger('book')



def search(request):
    keyword = request.GET.get('keyword', '')
    if keyword:
        # Filter items by name or category that contain the keyword (case-insensitive)
        items = Item.objects.filter(
            Q(name__icontains=keyword) | Q(category__icontains=keyword)
        )
    else:
        # If no keyword provided, display all items
        items = Item.objects.all()
    return render(request, 'search.html', {'items': items})