from datetime import datetime

from django.shortcuts import render, get_object_or_404

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    COUNT_OF_POSTS = 5
    current_time = datetime.now()
    post_list = Post.objects.all().filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:COUNT_OF_POSTS]
    context = {
        'post_list': post_list
    }
    return render(request, template, context)


def get_published_posts():
    current_time = datetime.now()
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=current_time
    )


def post_detail(request, id: int):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_published_posts(),
        id=id,
        category__is_published=True
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug: str):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_published_posts().filter(category=category)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
