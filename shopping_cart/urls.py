from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:pk>/', views.del_from_cart, name='del_from_cart'),
    path('cart-details', views.cart_details, name='cart-details'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/<order_id>', views.process_payment, name='process-payment'),
    path('update_records/<int:order_id>/', views.update_transaction_record, name='update-records'),
]