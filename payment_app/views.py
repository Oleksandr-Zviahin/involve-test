from flask import Blueprint, request, render_template
from payment_app.domain import CURRENCY

payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/", methods=["GET", "POST"])
def payment_form():
    if request.method == "GET":
        return render_template("payment_form.html")

    if request.method == "POST":
        request_data = request.form.to_dict()

        payment_type = CURRENCY.get(request_data["currency"])
        if payment_type:
            payment = payment_type(**request_data)
            return payment.process()

        return "There is no implementation for chosen currency"
