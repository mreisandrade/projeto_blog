from django.db import models

from utils.model_validators import validate_png
from utils.images import resize_image


class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    # Campo de imagem que corresponde a logo do site
    favicon = models.ImageField(
        # Necessário fornecer o local de armazenamento da imagem
        # Lembrando que ficará dentro da pasta "media"
        upload_to='assets/favicon/%Y/%m',
        # Campo não é obrigatório 
        blank=True,
        # Valor padrão
        default='',
        # Validadores do campo - deve ser um iterável
        validators=[
            # Verifica se a imagem enviada é PNG
            validate_png,
        ]
    )

    # Sobreescrevendo o método que salva os dados
    # Assim, pode-se fazer algo antes ou depois de salvar os dados
    def save(self, *args, **kwargs):
        # Pegando o favicon atual - string
        current_favicon_name = str(self.favicon.name)

        # É necessário chamar o super do método
        # Para salvar os dados
        super().save(*args, **kwargs)

        favicon_changed = False

        # Verifica se já favicon
        if self.favicon:
            favicon_changed = self.favicon.name != current_favicon_name

        # Verifica se o favicon for alterado
        if favicon_changed:
            # Redimensiona a imagem para ter largura de 32px 
            resize_image(self.favicon, new_width=32)


    def __str__(self):
        return self.title
    

# Create your models here.
class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)
    # Permitir colocar caminhos, urls, id, etc
    url_or_path = models.CharField(max_length=2048)
    # Abri o url em uma outra aba ou não
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        SiteSetup,
        # O que será feito quando o site_setup for apagado
        on_delete=models.CASCADE,
        # Campo não é obrigatório 
        blank=True,
        # Campo poder estar vazio 
        null=True,
        # Valor padrão
        default=None,
    )
