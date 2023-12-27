from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import  require_GET


@require_GET
def get_article(request, article_name):
    return render(request, f'public/documentation/articles/{article_name}.html')