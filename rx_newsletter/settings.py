import os
import redis
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDIS_HOST = "localhost"
REDIS_PORT = "6379"
REDIS_DB = 0
REDIS_NEWS_LIST_ID = "email_news"

EMAIL_HOST = os.environ["email"]
EMAIL_PASSWORD = os.environ["password"]
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_PORT = 465


NEWLETTER_TEMPLATE_PATH = "rx_newsletter/newletter_template.html"

def get_redis_connection(self):
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)