from typing import Any

# from django.core.paginator import Paginator
# from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
# Usado para condicionais com OU no Django
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404, HttpRequest, HttpResponse
# Para usar Classes Based Views no Django
from django.views.generic import ListView, DetailView

from blog.models import Post, Page


PER_PAGE = 9

'''
Funtion Based Views -> São funções
    - Mais usadas em aplicações simples
Class Based Views -> São classes (POO)
    - Para lógicas mais complicadas
    - Deixa o código mais limpo, simples e fácil de testar
    - Permite reutilizar código

Obs.: As classes based views do Django JÁ TEM PAGINAÇÃO, ou 
não é necessário implementar isso, como foi feito anteriormente.

Link para classes base do Django:
https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/
    - DetailView: 1 valor
    - ListView: lista de valores
'''


# def index(request):
#     # Posts
#     # Os parênteses são usados apenas para quebrar a linha
#     # posts = (
#     #     Post
#     #     .objects
#     #     .filter(is_published=True)
#     #     .order_by('-pk')
#     # )
#     posts = Post.objects.get_published() # type: ignore

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': 'Home - ',
#         },
#     )

# Class Based View equivalente a função "index"
class PostListView(ListView):
    # É necessário informar o model que está sendo usado
    # model = Post
    # Configurando a ordenação
    # ordering = '-pk',
    # Neste caso, não foi necessário inforamr o model nem 
    # o ordering pois já foi configurado a queryset

    # Por padrão, o Django tenta carregar um template padrão
    # Por tanto, é necessário alterar o template
    # Dica: Use seus próprios nomes, não os padrões do Django,
    # neste caso
    template_name = 'blog/pages/index.html'
    # Definindo o nome do contexto enviado para o template
    # Variável dentro do context
    # Onde serão buscado os dados no template
    context_object_name = 'posts'
    
    # A paginação já está pronta no Class Based View
    # É necessário apenas informar quanto elementos por página
    paginate_by = PER_PAGE
    # Definindo a QuerySet filtrar apenas os posts que estão 
    # publicados. Outra forma é sobreescrever o método
    # get_queryset(), como mostrado abaixo
    queryset = Post.objects.get_published() # type: ignore


    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # print()
        # print(context)
        # print()

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': 'Home - ',
            }
        )

        return context
    

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    # def get_queryset(self):
    #     queryset =  super().get_queryset()
    #     queryset = queryset.filter(is_published=True)
    #     return queryset
    

# def created_by(request, author_pk):
#     # Buscando o usuário no model User
#     user = User.objects.filter(pk=author_pk).first()
    
#     if user is None:
#         raise Http404()
    
#     user_full_name = user.username
#     if user.first_name:
#         user_full_name = f'{user.first_name} {user.last_name}'

#     page_title = f'Posts de {user_full_name} - '

#     # Posts
#     # Os parênteses são usados apenas para quebrar a linha
#     posts = (
#         Post
#         .objects
#         .get_published() # type: ignore
#         # Os __ significa que está pegando o campo pk do created_by
#         # (foreign key), neste caso
#         .filter(created_by__pk=author_pk)
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         },
#     )

# Class Based View equivalente a função "created_by"
class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    # Sobrescrevendo o método get para retornar uma HTTP404
    # caso o usuário não exista
    # O método get deve retornar um HTTP response
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # self.kwargs contém as variáveis que são enviadas
        # para a view pela URL (link em urls.py)
        # print()
        # print('ARGUMENTOS', self.kwargs)
        # print()

        # Buscando o usuário no model User
        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()
        
        if user is None:
            raise Http404()
            # Exemplo de redirecionar, não levar um Erro404   
            # return redirect('blog:index')

        # Atualizando o contexto com o título da página
        self._temp_context.update(
            {
                'author_pk': author_pk,
                'user': user,
            }
        )
        
        return super().get(request, *args, **kwargs)


    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pegando o user que vem do método get
        # O get é executado antes do get_context_data
        user = self._temp_context['user']
        
        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'

        page_title = f'Posts de {user_full_name} - '

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': page_title,
            }
        )

        return context
    

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.filter(
            created_by__pk=self._temp_context['user'].pk,
        )
        return queryset


# def category(request, slug):
#     # Posts
#     # Os parênteses são usados apenas para quebrar a linha
#     # Os __ significa que está pegando o campo slug da category
#     # (foreign key), neste caso
#     posts = (
#         Post
#         .objects
#         .get_published() # type: ignore
#         .filter(category__slug=slug)
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].category.name} - Categoria - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         },
#     )


# Class Based View equivalente a função "category"
class CategoryListView(PostListView):
    # Apresenta um erro caso não haja objetos a serem exibidos
    allow_empty = False

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.filter(
            category__slug=self.kwargs.get('slug'),
        )
        return queryset
    

    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = f'{self.object_list[0].category.name} - Categoria - ' # type: ignore

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': page_title,
            }
        )

        return context


# def tag(request, slug):
#     # Posts
#     # Os parênteses são usados apenas para quebrar a linha
#     # Os __ significa que está pegando o campo slug da tag
#     # (foreign key), neste caso
#     posts = (
#         Post
#         .objects
#         .get_published() # type: ignore
#         .filter(tags__slug=slug)
#     )

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f'{page_obj[0].tags.first().name} - Tag - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


# Class Based View equivalente a função "tag"
class TagListView(PostListView):
    # Apresenta um erro caso não haja objetos a serem exibidos
    allow_empty = False

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    def get_queryset(self):
        queryset =  super().get_queryset()
        queryset = queryset.filter(
            tags__slug=self.kwargs.get('slug'),
        )
        return queryset
    

    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_title = f'{self.object_list[0].tags.first().name} - Tag - ' # type: ignore

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': page_title,
            }
        )

        return context


# def search(request):
#     search_value = request.GET.get('search', '').strip()

#     # Posts
#     # Os parênteses são usados apenas para quebrar a linha
#     # Os __ significa que está pegando o campo slug da tag
#     # (foreign key), neste caso
#     posts = (
#         Post
#         .objects
#         .get_published() # type: ignore
#         .filter(
#             # Dessa forma, seria o AND
#             # title__icontains=search_value
#             # Título contém search_value OU
#             # O Q possibilita condicionais com o OU (|)
#             Q(title__icontains=search_value) |
#             # Excerto contém search_value OU
#             Q(excerpt__icontains=search_value) |
#             # Conteúdo contém search_value
#             Q(content__icontains=search_value)
#         )[0:PER_PAGE] # Pega apenas 9 valores
#     )

#     # Pega, no máximo, 30 caracteres
#     page_title = f'{search_value[:30]} - Search - '

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#             'page_title': page_title,
#         },
#     )


# Class Based View equivalente a função "search"
class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        

    # Sobrescrevendo o método realiza as configurações iniais
    def setup(self, request, *args, **kwargs):
        # Neste momento, o self.request ainda não está disponível
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar os posts com base no campo de pesquisa
    def get_queryset(self):
        search_value = self._search_value

        return super().get_queryset().filter(
            # Dessa forma, seria o AND
            # title__icontains=search_value
            # Título contém search_value OU
            # O Q possibilita condicionais com o OU (|)
            Q(title__icontains=search_value) |
            # Excerto contém search_value OU
            Q(excerpt__icontains=search_value) |
            # Conteúdo contém search_value
            Q(content__icontains=search_value)
        )[0:PER_PAGE] # Pega apenas 9 valores
    

    # Sobrescrevendo o método get 
    # O método get deve retornar um HTTP response
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value.strip() == '':
            return redirect('blog:index')
        
        return super().get(request, *args, **kwargs)
    

    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_value = self._search_value
        page_title = f'{search_value[:30]} - Search - '

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': page_title,
                'search_value': search_value,
            }
        )

        return context


# def page(request, slug):
#     # Pegando o post
#     page_object = (
#         Page.objects
#         .filter(is_published=True)
#         .filter(slug=slug)
#         .first() 
#     ) # type: ignore

#     if page_object is None:
#         raise Http404()

#     page_title = f'{page_object.title} - Página - '

#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page': page_object,
#             'page_title': page_title,
#         },
#     )


# Class Based View equivalente a função "page"
class PageDetailView(DetailView):
    # É necessário informar o model que está sendo usado
    model = Page

    # Por padrão, o Django tenta carregar um template padrão
    # Por tanto, é necessário alterar o template
    # Dica: Use seus próprios nomes, não os padrões do Django,
    # neste caso
    template_name = 'blog/pages/page.html'
    # Definindo o nome do contexto enviado para o template
    # Variável dentro do context
    # Onde serão buscado os dados no template
    context_object_name = 'page'
    # Campo do slug
    slug_field = 'slug'


    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtendo a dado mostrado na DetailView
        page_object = self.get_object() 
        page_title = f'{page_object.title} - Página - ' # type: ignore

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': page_title,
            }
        )

        return context
    

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    def get_queryset(self):
        return super().get_queryset().filter(
           is_published=True, 
        )


# def post(request, slug):
#     # Pegando o post
#     post_object = Post.objects.get_published().filter(slug=slug).first() # type: ignore

#     if post_object is None:
#         raise Http404()

#     page_title = f'{post_object.title} - Post - '

#     return render(
#         request,
#         'blog/pages/post.html',
#         {
#             'post': post_object,
#             'page_title': page_title,
#         },
#     )


# Class Based View equivalente a função "post"
class PostDetailView(DetailView):
    # É necessário informar o model que está sendo usado
    model = Post

    # Por padrão, o Django tenta carregar um template padrão
    # Por tanto, é necessário alterar o template
    # Dica: Use seus próprios nomes, não os padrões do Django,
    # neste caso
    template_name = 'blog/pages/post.html'
    # Definindo o nome do contexto enviado para o template
    # Variável dentro do context
    # Onde serão buscado os dados no template
    context_object_name = 'post'
    # Campo do slug
    slug_field = 'slug'


    # Sobrescrevendo o método que opera o contexto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtendo a dado mostrado na DetailView
        post_object = self.get_object() 
        post_title = f'{post_object.title} - Página - ' # type: ignore

        # Atualizando o contexto com o título da página
        context.update(
            {
                'page_title': post_title,
            }
        )

        return context
    

    # Sobrescrevendo o método que opera a QuerySet
    # Para filtrar apenas os posts que estão publicados
    def get_queryset(self):
        return super().get_queryset().filter(
           is_published=True, 
        )
