import string
from random import SystemRandom
from django.utils.text import slugify


# Cria um conjunto de letras + números aleatórios
def random_letters(k=5):
    return ''.join(
        SystemRandom().choices(
            # Conjuto de escolha - letras + números
            # string.ascii_letters + string.digits,
            string.ascii_lowercase + string.digits,
            # Quantidade de elementos
            k=k,
        )
    )


# Transforma em slug (aceitável para URL)
def slugify_new(text, k=5):
    return slugify(text) + '-' + random_letters(k)


# print(slugify_new('esse é o texto de exemplo'))
