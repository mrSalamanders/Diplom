import os
import random
from django.db import models
from django.db.models.signals import pre_save
from ecommerce.utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    new_filename = random.randint(1, 123123123123)
    final_name = f"{new_filename}{ext}"
    return f"products/{final_name}"


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)  # Products.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(blank=True, verbose_name='Ярлык')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=20, decimal_places=4, default=39.99, verbose_name='Цена')
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='Картинка')
    featured = models.BooleanField(default=False, verbose_name='Рекомендован?')
    active = models.BooleanField(default=False, verbose_name='Активен?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    # Manager
    objects = ProductManager()

    def get_absolute_url(self):
        # return f"/products/detail/{self.slug}/"
        return reverse('products:detail', kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["title"]


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)  # Signals



