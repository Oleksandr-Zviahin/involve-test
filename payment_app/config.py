import os
import logging

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    filename=os.path.join(BASEDIR, "payment_logs.log"),
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s: [%(levelname)s]: %(message)s",
)

logger = logging.getLogger()


class Config:
    DEBUG = os.environ.get("DEBUG", True)
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", 'sqlite:///' + os.path.join(BASEDIR, 'payment_app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "SecretKey01")
    SHOP_ID = os.environ.get("SHOP_ID", "5")
    SHOP_ORDER_ID = os.environ.get("SHOP_ORDER_ID", '101')
    PAYWAY = os.environ.get("PAYWAY", "payeer_rub")
