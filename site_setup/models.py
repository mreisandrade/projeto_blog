from django.db import models


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
