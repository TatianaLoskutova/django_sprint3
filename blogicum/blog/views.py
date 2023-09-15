from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound

from datetime import datetime

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    current_time = datetime.now()
    post_list = Post.objects.all().filter(
            pub_date__lte=current_time,
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')[0:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, id: int):
    template = 'blog/detail.html'
    current_time = datetime.now()
    post = get_object_or_404(
        Post,
        id=id,
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug: str):
    template = 'blog/category.html'
    current_time = datetime.now()
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
        )
    if not category.is_published:
        return HttpResponseNotFound('Категория не найдена')
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
