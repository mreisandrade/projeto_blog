from django.db import models

from utils.rands import slugify_new


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
