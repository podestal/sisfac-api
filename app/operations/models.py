from django.db import models
# from django.conf import settings
from django.core.exceptions import ValidationError

# inventario

class Business(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    sol_key = models.CharField(max_length=255, null=True, blank=True)
    ruc = models.CharField(max_length=11, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):

    UNIT_OF_MEASUREMENT_CHOICES = [
        ('KG', 'Kilogramo'),
        ('G', 'Gramo'),
        ('L', 'Litro'),
        ('ML', 'Mililitro'),
        ('U', 'Unidad'),
        ('B', 'Bolsa'),
        ('BX', 'Caja'),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measurement = models.CharField(choices=UNIT_OF_MEASUREMENT_CHOICES, max_length=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        # Only validate if both are set
        if self.business_id and self.category_id:
            if self.category.business_id != self.business_id:
                raise ValidationError({
                    "category": "This category belongs to a different business."
                })

    def save(self, *args, **kwargs):
        # Ensures validation runs even when not using ModelForms
        self.full_clean()
        return super().save(*args, **kwargs)

# facturacion
# compras
