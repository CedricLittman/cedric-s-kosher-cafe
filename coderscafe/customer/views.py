"""
from django.shortcuts import render
from django.views import View
from .models import MenuItem, Category, OrderModel
# Create your views here.

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
            # get every item from category
            appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
            entres = MenuItem.objects.filter(category__name__contains='Entre')
            desserts = MenuItem.objects.filter(category__name__contains='Dessert')
            drinks = MenuItem.objects.filter(category__name__contains='Drink')

            # pass into context
            context = {
                'appetizers': appetizers,
                'entres': entres,
                'desserts': desserts,
                'drinks': drinks,
            }

            # render the template
            return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        order_items = {
            items: [],
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            
            order_items['items'].append(item_data)

            price = 0
            item_ids = []

            for item in order_items['items']:
                price += item['price']
                item_ids.append(item['id'])


            order = OrderModel.objects.create(price=price)
            order.items.add(*item_ids)

            context = {
                items: order.items['items'],
                price: price }
"""

from django.shortcuts import render
from django.views import View
from django.core.mail import send_mail 
from .models import MenuItem, OrderModel


class Index(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *arg, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *arg, **kwargs):
        # get all items from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

        price = 0
        item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price = price,
            name = name,
            email = email,
            street = street,
            city = city,
            state = state,
            postcode = postcode
        )

        order = OrderModel.objects.create(price=price)
        order.items.add(*item_ids)

        #Confirmation email sent to console
        body = (Thank you for your order. f'Your total is {price}')

        send_mail(
            'Many thanks for your order, we really yppreciate being eble to serve you',
            body,
            'joe@message.com',
            [email],
            fail_silently = False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }        

        return render(request, 'customer/order_confirmation.html', context)

        