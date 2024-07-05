import os
import django

from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()

from quoteapp.models import Author, Tag, Quote

client = MongoClient("mongodb://localhost:27017")

db = client.db_quotes

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname = author['fullname'],
        born_date = author['born_date'],
        born_location = author['born_location'],
        description = author['description']
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name = tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote = quote['quote'])))

    if not exist_quote:
        print(quote['author'])
        author = db.authors.find_one({'_id': quote['author']})
        print(author['_id'])
        a = Author.objects.filter(fullname = author['fullname']).first()
        print(a)
        q = Quote.objects.create(
            quote = quote['quote'],
            author = a
        )

        for tag in tags:
            q.tags.add(tag)