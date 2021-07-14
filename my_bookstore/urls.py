"""my_bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from my_bookstore.settings import DEBUG
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from bookstore_app import views
import bookstore_app
import accounts
import shopping_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.book_list, name='book_list'),
    path('books/', include('bookstore_app.urls', namespace='bookstore_app')),
    path('cart/', include('shopping_cart.urls', namespace='shopping_cart')),
    path('profiles/', include('accounts.urls', namespace='profile')),
    path('accounts/', include('allauth.urls')),
    # stripe urls
    path('success/', shopping_cart.views.success, name='success')
    
]


