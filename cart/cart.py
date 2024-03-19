from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавить товар в корзину либо обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()#чтобы сохранить корзину в сеансе.

    def save(self, ):
        '''
        Пометить сеанс как "измененный", чтобы обеспечить его сохранение
        '''
        self.session.modified = True #помечает сеанс как измененный

    def remove(self, product):
        '''
        Удалить товар из корзины
        '''
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]#Удаляем товар из словаря 'cart'
            self.save() #чтобы обновить корзину в сеансе.

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.pk)]['product'] = product
        for item in cart.values():
            item['price'] = float(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item #возвращает словарь на каждой итерации цикла.

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())
        #Возвращается сумма всех товаров  корзине

    def get_total_price(self):
        '''
         Расчета общей стоимости товаров в корзине
        '''
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del  self.session[settings.CART_SESSION_ID]
        self.save()