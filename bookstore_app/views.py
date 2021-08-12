from django.shortcuts import render, redirect
from .models import Book
from shopping_cart.models import Order
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# Create your views here.
def book_list(request):
    current_books = []
    books = Book.objects.all()
    try:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_submitted=False)
        user_order = filtered_orders[0]
        our_orderitems = user_order.items.all()    
        for item in our_orderitems:
            current_books.append(item.book)
    except: 
         user_order=None
        
    context = {
        'books':books,
        'current_books':current_books,
        'user_order': user_order
    }
    return render(request, 'book_list.html', context)

@login_required
def make_author(request):
    g = Group.objects.get(name='Author')
    if request.method == 'POST':
        if 'author' in request.POST:
            is_author = request.POST['author']
            if is_author:
                g.user_set.add(request.user)
                g.save
        else:
            g.user_set.remove(request.user)
            g.save
    return redirect('bookstore_app:book_list')
