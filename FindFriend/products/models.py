from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    src = models.CharField(max_length=255)
    parent = models.ForeignKey('Category', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    src = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'src', 'price',]
