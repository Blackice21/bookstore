from django.db import models
from accounts.models import Profile
from bookstore_app.models import Book
import datetime
import re

# Create your models here.
class OrderItem(models.Model):
    book = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def __str__(self):
          return self.book.title

class Order(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(OrderItem)
    is_submitted = models.BooleanField(default=False)
    barcode = models.CharField(max_length=200)
    date_submitted = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
       return sum([item.book.price for item in self.items.all()])
            
    def __str__(self):
        return '{name} -- {barcode}'.format(name=self.owner.name, barcode=self.barcode)

    # returns a bar code using the current year,month,day,hour,min,microsecond
    def get_bar_code():
        b_code = ''
        curr_time = str(datetime.datetime.now())
        random_numbers = re.findall('\d',curr_time)
        for num in random_numbers: b_code = b_code+num
        return b_code
