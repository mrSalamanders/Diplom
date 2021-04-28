from django.db import models
from billing.models import BillingProfile


ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=False, on_delete=models.SET_NULL, verbose_name='Платёжный адрес')
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES, verbose_name='Тип адреса')
    address_line_1 = models.CharField(max_length=120, verbose_name='Строка адреса 1')
    address_line_2 = models.CharField(max_length=120, null=True, blank=True, verbose_name='Строка адреса 2')
    city = models.CharField(max_length=120, verbose_name='Город или населенный пункт')
    country = models.CharField(max_length=120, default='Россия', verbose_name='Страна')
    state = models.CharField(max_length=120, verbose_name='Федеративная единица или штат')
    postal_code = models.CharField(max_length=120, verbose_name='Почтовый индекс')

    def __str__(self):
        return str(self.billing_profile) + ' : ' + str(self.address_type).upper()

    def get_address(self):
        return f"{self.address_line_1} {self.address_line_2 or ''} / {self.state}, {self.city} {self.postal_code} {self.country}"

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адресы"
