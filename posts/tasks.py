from celery import shared_task
import os
import json


from dotenv import load_dotenv
from requests import get
from datetime import datetime, timedelta
from posts.models import Post, User

load_dotenv()


API_KEY = os.getenv('NEWSAPI_KEY')
today = datetime.now()
yesterday = datetime.now() - timedelta(days=1)
date = yesterday.strftime('%Y-%m-%d')


@shared_task()
def get_news(query):
    url = f'https://newsapi.org/v2/everything?q={query}&from={date}&to={date}&sortBy=popularity&apiKey={API_KEY}&language=ru'
    if not User.objects.filter(username=f'{query}_bot').exists():
        User.objects.create(username=f'{query}_bot')
    response = get(url).text
    response = json.loads(response)
    if response['totalResults'] != 0:
        articles = response['articles']
        result = []
        for article in articles:
            article_text = f"{article['title']} \n{article['description']} \n{article['url']} \n "
            result.append(Post(text=article_text, author=User.objects.get(username=f'{query}_bot')))
        Post.objects.bulk_create(result)
