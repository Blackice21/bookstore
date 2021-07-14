from accounts.models import Profile
from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from bookstore_app.models import Book
from .models import Order, OrderItem
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
# what to do?
# add to cart, del from cart, detail into cart

def get_current_order(request):
    # gets the current order from the user 
    user_order = Order.objects.filter(owner=request.user.profile, is_submitted=False)
    if user_order.exists():
        return user_order[0]
    else:
        return None

@login_required
def add_to_cart(request, pk):
    # get user product
    user_book = get_object_or_404(Book, pk=pk)

    user_order_item, status = OrderItem.objects.get_or_create(book=user_book)
    user_order, status = Order.objects.get_or_create(owner=request.user.profile, is_submitted=False)
    user_order.items.add(user_order_item)
    
    if user_book in request.user.profile.my_ebooks.all():
        return render(request, 'book_list.html', {'message':'already bought'})

    if status:
        user_order.bar_code = Order.get_bar_code()
        user_order.save()
    
    # message
    return redirect(reverse('bookstore_app:book_list'))

def del_from_cart(request, pk):
    user_orderitem = get_object_or_404(OrderItem,pk=pk)
    user_orderitem.delete()
    # message
    return redirect(reverse('bookstore_app:book_list'))

def cart_details(request):
    current_order = get_current_order(request)
    return render(request, 'cart_detail.html',{'current_order':current_order})

def checkout(request):
    current_order = get_current_order(request)
    return render(request, 'checkout.html',{'current_order':current_order})

def process_payment(request, order_id):
      # Stripe config here
      order = get_object_or_404(Order, id=order_id)
      YOUR_DOMAIN = "http://127.0.0.1:8000"
      checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(order.get_cart_total()*100),
                        'product_data': {
                            'name': 'Your order',
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                "order_id": order_id
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
      return redirect(checkout_session.url, code=303)

def success(request):
   current_order = get_current_order(request) 
   return redirect(reverse('shopping_cart:update-records', kwargs={'order_id':current_order.id}))

def update_transaction_record(request, order_id):
    # get logged in user
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the purchased order and update its records
    submitted_order = Order.objects.filter(pk=order_id).first()
    submitted_order.is_submitted = True
    submitted_order.date_ordered = datetime.now()
    submitted_order.save()
    # get purchased items from the order and update records as well
    ordered_items = submitted_order.items.all()
    ordered_items.update(is_ordered=True, date_ordered=datetime.now())
    ordered_Book = [item.book for item in ordered_items]
    user_profile.my_ebooks.add(*ordered_Book)
    user_profile.save()
    return redirect(reverse('profile:my_profile'))

