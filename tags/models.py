from django.db import models
from django.db.models.signals import pre_save
from ecommerce.utils import unique_slug_generator
from products.models import Product
from colorfield.fields import ColorField


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name='Наименование')
    color = ColorField(default='#FF0000', verbose_name='Цвет')
    slug = models.SlugField(blank=True, verbose_name='Ярлык')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    active = models.BooleanField(default=True, verbose_name='Активен?')
    products = models.ManyToManyField(Product, blank=True, verbose_name='Товары')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Tag)  # Signals