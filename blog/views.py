from django.core.paginator import Paginator
from django.shortcuts import render

from blog.models import Post


PER_PAGE = 9


def index(request):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    # posts = (
    #     Post
    #     .objects
    #     .filter(is_published=True)
    #     .order_by('-pk')
    # )
    posts = Post.objects.get_published() # type: ignore

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def created_by(request, author_pk):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    posts = (
        Post
        .objects
        .get_published() # type: ignore
        # Os __ significa que está pegando o campo pk do created_by
        # (foreign key), neste caso
        .filter(created_by__pk=author_pk)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def category(request, slug):
    # Posts
    # Os parênteses são usados apenas para quebrar a linha
    # Os __ significa que está pegando o campo slug da category
    # (foreign key), neste caso
    posts = (
        Post
        .objects
        .get_published() # type: ignore
        .filter(category__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )


def page(request, slug):
    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )


def post(request, slug):
    # Pegando o post
    post = Post.objects.get_published().filter(slug=slug).first() # type: ignore

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )
