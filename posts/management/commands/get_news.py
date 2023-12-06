import os
import json


from dotenv import load_dotenv
from requests import get
from datetime import datetime, timedelta
from django.core.management import BaseCommand
from posts.models import Post, User

load_dotenv()


API_KEY = os.getenv('NEWSAPI_KEY')
today = datetime.now()
yesterday = datetime.now() - timedelta(days=1)
date = yesterday.strftime('%Y-%m-%d')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('query')

    def handle(self, *args, **options):
        query = options['query']
        url = f'https://newsapi.org/v2/everything?q={query}&from={date}&to={date}&sortBy=popularity&apiKey={API_KEY}&language=ru'
        if not User.objects.filter(username=f'{query}_bot').exists():
            User.objects.create(username=f'{query}_bot')
        response = get(url).text
        response = json.loads(response)
        articles = response['articles']
        result = []
        for article in articles:
            article_text = f"{article['title']} \n{article['description']} \n{article['url']} \n "
            result.append(Post(text=article_text, author=User.objects.get(username=f'{query}_bot')))
        Post.objects.bulk_create(result)
