import datetime
import requests
import datetime as dt
import random
from twilio.rest import Client


STOCK_DATA_API = "JATYXPBB3VXWUV3M"
NEWS_DATA_API = "9c5bdc74276d45a082f193dc425196cd"
account_sid = 'AC30664fa8a8dffe50100aca36d74ea3e2'
auth_token = '46acd0916d3affdf38c394b6d11cc08a'
stock_high = "📈"
stock_low = "📉"
day = dt.datetime.today()
today = day.date()
yesterday = today - datetime.timedelta(days=1)
day_before_yesterday = yesterday - datetime.timedelta(days=1)

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {"function": "TIME_SERIES_INTRADAY",
                "symbol": "TSLA",
                "interval": "60min",
                "outputsize": "full",
                "apikey": STOCK_DATA_API,

                }

news_params = {"q": "Tesla",
               "apikey": NEWS_DATA_API,
               "from": today,
               "language": "en"

               }
stock_response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_high_yesterday = float(stock_response.json()["Time Series (60min)"]
                             [f"{yesterday} 20:00:00"]["2. high"])
stock_high_day_before = float(stock_response.json()["Time Series (60min)"]
                              [f"{day_before_yesterday} 20:00:00"]["2. high"])


def get_news():
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    news_response.raise_for_status()
    news_data = random.choice(news_response.json()["articles"])
    title = news_data["title"]
    desc = news_data["description"]
    return title, desc


def send_message(news_title, news_desc, stocks, percent):
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
                body=f"TSLA {stocks} {percent}%.\nHeadline:{news_title}\nBrief:{news_desc}",
                from_='+13213390418',
                to='+919740118905'
                )

    print(message.sid)


if stock_high_yesterday > stock_high_day_before:
    increase = round(((stock_high_yesterday - stock_high_day_before) / stock_high_day_before) * 100)
    if increase > 0:
        new_title = get_news()[0]
        new_desc = get_news()[1]
        send_message(news_title=new_title, news_desc=new_desc, stocks=stock_high, percent=increase)
else:
    decrease = round(((stock_high_day_before - stock_high_yesterday)/stock_high_day_before) * 100)
    if decrease > 0:
        new_title = get_news()[0]
        new_desc = get_news()[1]
        send_message(news_title=new_title, news_desc=new_desc, stocks=stock_low, percent=decrease)
