from django.shortcuts import render
from .models import Book
from shopping_cart.models import Order

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
