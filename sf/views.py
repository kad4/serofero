from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404

from .models import Category, Page

from classifier.classifier import categories

category_list = categories

def index(request):
    page_list = Page.objects.order_by('pub_date')[:8]
    top_page_list = Page.objects.order_by('views')[:4]
    first_page = page_list[0]

    context_dict = {'categories': category_list, 'pages': page_list, 'top_pages': top_page_list, 'first_page':first_page}
    return render(request, 'sf/index.html', context_dict)

def category(request, category_name_slug):
    category=get_object_or_404(Category, slug=category_name_slug)

    page_list = Page.objects.filter(category=category).order_by('pub_date')

    context_dict = {'category': category, 'pages': page_list, 'categories':category_list}
    return render(request, 'sf/category.html', context_dict)

def page(request, pk):
    page=get_object_or_404(Page, id=pk)

    context_dict = {'page': page, 'categories':category_list}
    return render(request, 'sf/page.html', context_dict)
