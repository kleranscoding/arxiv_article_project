from django.shortcuts import render
from . import arxiv_api_model as aam

# Create your views here.

## index page
def index(request):
    # return the home page template
    return render(request,'arxiv_article_app/home.html')

## fetch articles
def get_articles(request):
    article_id = request.GET.get('article_id', None)
  
    entry_list = aam.get_articles(article_id)
  
    if article_id:
        return render(request, 'arxiv_article_app/article.html', {'entry': entry_list[0]})
    return render(request, 'arxiv_article_app/articles.html', {'entries': entry_list})

## fetch authors
def get_authors(request):
    author = request.GET.get('author', None)
    
    if author:
        entry_list = aam.get_author_details(author)
        return render(request, 'arxiv_article_app/author.html', {'author': author, 'entries': entry_list})
    else:
        author_list = aam.get_authors_list()
        return render(request, 'arxiv_article_app/authors.html', {'authors': author_list})

  

