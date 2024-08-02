import stripe
from django.urls import reverse
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_payment_session(request):
    """Сессия для оплаты"""

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': "Пожизненная подписка",
                },
                'unit_amount': 1000 * 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('users:success_subscription')),
        cancel_url=request.build_absolute_uri(reverse('users:cancel_subscription')),
    )

    return session
