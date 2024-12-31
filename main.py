import os
from twilio.rest import Client
import requests

ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
FROM_WHATSAPP_NUM = os.environ.get("FROM_WHATSAPP_NUM")
TO_WHATSAPP_NUM = os.environ.get("TO_WHATSAPP_NUM")
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = os.environ.get("STOCK_ENDPOINT")
NEWS_ENDPOINT = os.environ.get("NEWS_ENDPOINT")
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

diff_amount = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if diff_amount > 2:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((diff_amount / float(yesterday_closing_price)) * 100)

if abs(diff_percent) > 2:
    news_param = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_param)
    article = news_response.json()["articles"]
    three_articles = article[:3]

    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    article_list = [(f"{up_down}{diff_percent}:{STOCK_NAME}\nHeadline: {article['title']}\n"
                     f" Brief: {article['description']}") for article in three_articles]

    for article in article_list:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            from_=f'whatsapp:{FROM_WHATSAPP_NUM}',
            body=article,
            to=f'whatsapp:{TO_WHATSAPP_NUM}'
        )
