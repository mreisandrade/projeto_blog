from django.db import models
# Usuário padrão do Django
from django.contrib.auth.models import User
# Para Django Summernote
from django_summernote.models import AbstractAttachment

from utils.rands import slugify_new
from utils.images import resize_image


# Classe usada para o Summernote
# Criada basicamente para sobreescrever o métodos save e 
# redimensionar as imagens enviadas
class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

         # Pegando o cover atual - string
        current_file_name = str(self.file.name)

        # É necessário chamar o super do método
        # Para salvar os dados
        super_save = super().save(*args, **kwargs)

        file_changed = False

        # Verifica se há cover
        if self.file:
            file_changed = self.file.name != current_file_name

        # Verifica se cover for alterado
        if file_changed:
            # Redimensiona a imagem para ter largura de 900px 
            resize_image(self.file, new_width=900, quality=70)

        return super_save


# Create your models here.
# Tags dos posts
class Tag(models.Model):
    # Configurações do model
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    # Campos do model
    # Nome da tag
    name = models.CharField(max_length=255)
    # Texto que vai representar a tag na URL (parecido com id)
    slug = models.SlugField(
        # Atribuindo com único
        unique=True,
        # Valor padrão
        default=None,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
        # Tamanho máximo 
        max_length=255,
    )


    # Nome que é exibido ao chamar o model
    def __str__(self) -> str:
        return self.name


    # Sobreescrevendo o método que salva os dados
    # Assim, pode-se fazer algo antes ou depois de salvar os dados
    def save(self, *args, **kwargs):
        # Se não existir uma slug
        if not self.slug:
            # Cria a slug
            self.slug = slugify_new(self.name)

        # É necessário chamar o super do método
        # Para salvar os dados
        super().save(*args, **kwargs)


# Categoria dos posts
class Category(models.Model):
    # Configurações do model
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    # Campos do model
    # Nome da categoria
    name = models.CharField(max_length=255)
    # Texto que vai representar a categoria na URL 
    # (parecido com id)
    slug = models.SlugField(
        # Atribuindo com único
        unique=True,
        # Valor padrão
        default=None,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
        # Tamanho máximo 
        max_length=255,
    )


    # Nome que é exibido ao chamar o model
    def __str__(self) -> str:
        return self.name


    # Sobreescrevendo o método que salva os dados
    # Assim, pode-se fazer algo antes ou depois de salvar os dados
    def save(self, *args, **kwargs):
        # Se não existir uma slug
        if not self.slug:
            # Cria a slug
            self.slug = slugify_new(self.name)

        # É necessário chamar o super do método
        # Para salvar os dados
        super().save(*args, **kwargs)


# Páginas do blog (segue a estrutura do blog, mas com o conteúdo
# em HTML provido a parte)
class Page(models.Model):
    # Configurações do model
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    # Título da página
    title = models.CharField(max_length=64)
    # Texto que vai representar a página na URL (parecido com id)
    slug = models.SlugField(
        # Atribuindo com único
        unique=True,
        # Valor padrão
        default=None,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
        # Tamanho máximo 
        max_length=255,
    )
    is_published = models.BooleanField(
        # Valor padrão
        default=False,
        # Texto de ajuda
        help_text='Este campo precisará estar marcado para a página ser exibida publicamente'
    )
    content = models.TextField()


    # Nome que é exibido ao chamar o model
    def __str__(self) -> str:
        return self.title


    # Sobreescrevendo o método que salva os dados
    # Assim, pode-se fazer algo antes ou depois de salvar os dados
    def save(self, *args, **kwargs):
        # Se não existir uma slug
        if not self.slug:
            # Cria a slug
            self.slug = slugify_new(self.title)

        # É necessário chamar o super do método
        # Para salvar os dados
        super().save(*args, **kwargs)


# Extendendo o Manager do Django 
class PostManager(models.Manager):
    # Obter os posts publicados
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')


# Posts do blog 
class Post(models.Model):
    # Configurações do model
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


    # Manager padrão do Django - Não altera as funcionalidades
    # objects = models.Manager()
    # Manager extendido por mim
    objects = PostManager()

    # Título do post
    title = models.CharField(max_length=64)
    # Texto que vai representar a página na URL (parecido com id)
    slug = models.SlugField(
        # Atribuindo com único
        unique=True,
        # Valor padrão
        default=None,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
        # Tamanho máximo 
        max_length=255,
    )
    # Resumo do post
    excerpt = models.CharField(max_length=150)
    # Torna o post público apenas se for verdadeiro
    is_published = models.BooleanField(
        # Valor padrão
        default=False,
        # Texto de ajuda
        help_text='Este campo precisará estar marcado para a página ser exibida publicamente'
    )
    # Conteúdo do post (HTML)
    # Como instalar o Django Summernotes
    # https://github.com/lqez/django-summernote
    content = models.TextField()
    # Capa do posts
    cover = models.ImageField(
        # Onde será armazenado o arquivo
        # Na pasta ./media/post/<ano_atual>/<mês_atual>/
        upload_to='posts/%Y/%m/',
        # Aceita não definir valores
        blank=True,
        # Valor padrão
        default='',
    )
    # Atribui a exibição da imagem da capa também dentro do
    # conteúdo do post, ou não
    cover_in_post_content = models.BooleanField(
        # Valor padrão
        default=True,
        # Texto de ajuda
        help_text='Exibir a imagem da capa também dentro do conteúdo do post',
    )
    # Quando o post foi criado
    created_at = models.DateTimeField(
        # Adiciona a data atual quando o post for CRIADO
        auto_now_add=True,
    )
    # Quem criou o post
    created_by = models.ForeignKey(
        # model relacionado
        User,
        # O que fazer ao deletar o elemento da User
        on_delete=models.SET_NULL,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
        # Nome relacionado 
        # Pode ser acessado por user.post.title
        # Ou, da forma invertida, user.post_set.all(),
        # que, neste caso, fica user.page_created_by.all()
        related_name='page_created_by',
    )
    # Quando o post foi atualizado
    updated_at = models.DateTimeField(
        # Adiciona a data atual quando o post for ATUALIZADO
        auto_now=True,
    )
    # Quem atualizou o post
    updated_by = models.ForeignKey(
        # model relacionado
        User,
        # O que fazer ao deletar o elemento da User
        on_delete=models.SET_NULL,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
        # Nome relacionado 
        # Pode ser acessado por user.post.title
        # Ou, da forma invertida, user.post_set.all(),
        # que, neste caso, fica user.page_updated_by.all()
        related_name='page_updated_by',
    )
    # Categoria do post
    # Relação de muitos para um
    category = models.ForeignKey(   
        # model relacionado
        Category,
        # O que fazer ao deletar o elemento da Category
        on_delete=models.SET_NULL,
        # Valor padrão
        default=None,
        # Aceita valores nulos
        null=True,
        # Aceita não definir valores
        blank=True,
    )
    # Tag do post
    # Relação de muitos para muitos
    tags = models.ManyToManyField(
        # model relacionado
        Tag,
        # Valor padrão
        default='',
        # Aceita não definir valores
        blank=True,
    )


    # Nome que é exibido ao chamar o model
    def __str__(self) -> str:
        return self.title
    

    # Sobreescrevendo o método que salva os dados
    # Assim, pode-se fazer algo antes ou depois de salvar os dados
    def save(self, *args, **kwargs):
        # Se não existir uma slug
        if not self.slug:
            # Cria a slug
            self.slug = slugify_new(self.title)

        # Pegando o cover atual - string
        current_cover_name = str(self.cover.name)

        # É necessário chamar o super do método
        # Para salvar os dados
        super_save = super().save(*args, **kwargs)

        cover_changed = False

        # Verifica se há cover
        if self.cover:
            cover_changed = self.cover.name != current_cover_name

        # Verifica se cover for alterado
        if cover_changed:
            # Redimensiona a imagem para ter largura de 900px 
            resize_image(self.cover, new_width=900, quality=70)

        return super_save
