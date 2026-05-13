import stripe
from forex_python.converter import CurrencyRates
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name_product):
    """Создает продукт в страйпе"""

    return stripe.Product.create(name=name_product)


def convert_rub_to_dollars(amount):
    """Конвертация валюты"""

    c = CurrencyRates()
    rate = c.get_rate('RUB', "USD")
    return int(amount * rate)


def create_stripe_price(amount, product_id=None, product_name=None):
    """Создает цену в страйпе"""

    if product_id:
        return stripe.Price.create(
            currency="usd",
            unit_amount=int(amount * 100),
            product=product_id,
        )
    else:
        return stripe.Price.create(
            currency="usd",
            unit_amount=int(amount * 100),
            product_data={"name": product_name},
        )


def create_stripe_sessions(price):
    """Создает сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
