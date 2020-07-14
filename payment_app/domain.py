import hashlib
import requests
from abc import abstractmethod
from flask import current_app, render_template, redirect

from payment_app.config import logger
from payment_app.constant import EUR, USD, RUB
from payment_app.models import Payments, db


class PaymentHelper:
    fields = ()

    def __init__(self, **kwargs):
        self.currency = kwargs["currency"]
        self.shop_id = current_app.config["SHOP_ID"]
        self.shop_order_id = current_app.config["SHOP_ORDER_ID"]
        self.amount = kwargs["amount"]
        self.description = kwargs["description"]

    def create_sign(self):
        required_items = list()
        for key, value in self.__dict__.items():
            if key in self.fields:
                required_items.append((key, value))

        sorted_values = [i[1] for i in sorted(required_items)]
        sign_string = ":".join(sorted_values) + current_app.config["SECRET_KEY"]
        sign = hashlib.sha256(bytes(sign_string, 'utf-8')).hexdigest()
        return sign

    def save_payment_info(self):
        payment = Payments(
            shop_order_id=self.shop_order_id,
            currency=self.currency,
            amount=self.amount,
            description=self.description
        )
        db.session.add(payment)
        db.session.commit()

    @abstractmethod
    def get_pay_info(self, sign):
        pass

    @abstractmethod
    def process(self):
        pass


class Pay(PaymentHelper):
    fields = ('amount', 'currency', 'shop_id', 'shop_order_id')
    URL = "https://pay.piastrix.com/ru/pay"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_pay_info(self, sign):
        return {
            "url": self.URL,
            "method": "post",
            "data": {
                "amount": self.amount,
                "currency": self.currency,
                "shop_order_id": self.shop_order_id,
                "shop_id": self.shop_id,
                "description": self.description,
                "sign": sign,
            }
        }

    def process(self):
        logger.info("Payment with currency EUR")

        sign = self.create_sign()
        self.save_payment_info()
        return render_template("sending_payment.html", payment_info=self.get_pay_info(sign))


class Bill(PaymentHelper):
    fields = ("payer_currency", "shop_amount", "shop_currency", "shop_id", "shop_order_id")
    URL = "https://core.piastrix.com/bill/create"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payer_currency = kwargs["currency"]
        self.shop_amount = kwargs["amount"]
        self.shop_currency = kwargs["currency"]

    def get_pay_info(self, sign):
        return {
            "amount": self.amount,
            "currency": self.currency,
            "shop_order_id": self.shop_order_id,
            "shop_id": self.shop_id,
            "description": self.description,
            "payer_currency": self.payer_currency,
            "shop_amount": self.shop_amount,
            "shop_currency": self.shop_currency,
            "sign": sign
        }

    def process(self):
        logger.info("Payment with currency USD")

        sign = self.create_sign()
        response = requests.post(self.URL, json=self.get_pay_info(sign))

        if response.json()["error_code"] == 0:
            self.save_payment_info()
            return redirect(response.json()["data"]["url"])
        else:
            err = f"request failed, response: {response.json()}"
            logger.info(err)
            return err


class Invoice(PaymentHelper):
    fields = ('amount', 'currency', 'payway', 'shop_id', 'shop_order_id')
    URL = "https://core.piastrix.com/invoice/create"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payway = current_app.config["PAYWAY"]

    def get_pay_info(self, sign):
        return {
            "amount": self.amount,
            "currency": self.currency,
            "shop_order_id": self.shop_order_id,
            "shop_id": self.shop_id,
            "description": self.description,
            "payway": self.payway,
            "sign": sign
        }

    def process(self):
        logger.info("Payment with currency RUB")
        sign = self.create_sign()
        response = requests.post(self.URL, json=self.get_pay_info(sign))

        if response.json()["error_code"] == 0:
            self.save_payment_info()
            return render_template("sending_payment.html", payment_info=response.json()["data"])
        else:
            err = f"request failed, response: {response.json()}"
            logger.info(err)
            return err


CURRENCY = {
    EUR: Pay,
    USD: Bill,
    RUB: Invoice
}
