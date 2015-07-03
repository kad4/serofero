from django.http import HttpResponse
from django.shortcuts import render
from .models import Category, Page

def index(request):
    category_list = Category.objects.order_by('name')
    page_list = Page.objects.order_by('pub_date')[:8]
    top_page_list = Page.objects.order_by('views')[:4]
    first_page = page_list[0]

    context_dict = {'categories': category_list, 'pages': page_list, 'top_pages': top_page_list, 'first_page':first_page}
    response = render(request, 'sf/index.html', context_dict)

    return response

def category(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        category_list = Category.objects.order_by('name')
        page_list = Page.objects.filter(category=category).order_by('pub_date')
    except Category.DoesNotExist:
        return HttpResponse('Invalid Category')

    context_dict = {'category': category, 'pages': page_list, 'categories':category_list}
    response = render(request, 'sf/category.html', context_dict)

    return response

def page(request, pk):
    try:
        category_list = Category.objects.order_by('name')
        page = Page.objects.get(id=pk)
    except:
        return HttpResponse('Invalid Page')

    context_dict = {'page': page, 'categories':category_list}
    response = render(request, 'sf/page.html', context_dict)

    return response
