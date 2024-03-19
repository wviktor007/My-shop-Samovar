from decimal import Decimal
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order

# создаю экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # данные сеанса оформления платежа Stripe
        session_data = {
            'mode': 'payment',
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [],
            'payment_method_types': ['card']
        }
        # добавить товарные позиции заказа
        # в сеанс оформления платежа Stripe
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * 100),
                    'currency': 'KZT',
                    'product_data': {'name': item.product.name,},
                },
                'quantity': item.quantity,
            })
        # создать сеанс оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())


#'mode' режим сеанса оформления платежа, 'payment' - разовый платеж
#client_reference_id: уникальная ссылка для этого платежа
#success_url: URL-адрес, на который Stripe перенаправляет пользователя в случае успешного платежа
#build_absolute_uri(), чтобы формировать абсолютный
# URI-идентификатор из пути URL-адреса
# line_items: это пустой список. Далее он будет заполнен приобретаемыми позициями из заказа.


def payment_completed(request):
    '''
    Перенаправляет пользователя в случае успешного прохождения платежа
    '''
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    '''
    Перенаправляет пользователя в случае отмены платежа
    '''
    return render(request, 'payment/canceled.html')