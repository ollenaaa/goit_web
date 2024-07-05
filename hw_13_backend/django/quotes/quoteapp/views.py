from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from urllib.parse import unquote

  
# Create your views here.
from .models import Author, Tag, Quote
from .forms import AuthorForm, QuoteForm


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page=per_page)
    quotes_on_page = paginator.page(page)
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, "quoteapp/index.html", {"quotes" : quotes_on_page, "top_tags": top_tags})


def author(request, fullname):
    author_fullname = Author.objects.filter(fullname = fullname).first()
    author = get_object_or_404(Author, pk=author_fullname.id)
    return render(request, 'quoteapp/author.html', {"author": author})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_author.html', {'form': form})

    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm()})


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            author_fullname = request.POST.get('authors')
            author = Author.objects.get(fullname=author_fullname)
            new_quote.author = author

            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))

            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to='quoteapp:main')
        else:
            return render(request, 'quoteapp/add_quote.html', {'authors': authors, 'tags': tags, 'form': form})

    return render(request, 'quoteapp/add_quote.html', {'authors': authors, 'tags': tags, 'form': QuoteForm()})


def tag(request, name):
    tag_name = Tag.objects.filter(name = name).first()
    tag = get_object_or_404(Tag, pk=tag_name.id)
    quotes = Quote.objects.filter(tags=tag)
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    return render(request, 'quoteapp/tag.html', {"tag": tag, "quotes": quotes, "top_tags": top_tags})