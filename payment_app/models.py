from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Payments(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    shop_order_id = db.Column(db.String, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    effective_date = db.Column(db.DateTime, default=datetime.utcnow)
