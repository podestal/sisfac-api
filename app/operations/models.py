from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid

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
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
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

class Profile(models.Model):

    ROLE_CHOICES = [
        ("PR", "Propietario"),
        ("AD", "Administrador"),
        ("EM", "Empleado"),
        ("PA", "Administrador de la plataforma"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Obligatorio para todos los roles excepto Administrador de la plataforma"
    )
    role = models.CharField(max_length=2, choices=ROLE_CHOICES, default="EM")
    employee_id = models.CharField(max_length=50, blank=True, null=True, help_text="ID de empleado en el negocio")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Indica si el perfil está activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'business'],
                name='unique_user_business',
                condition=models.Q(business__isnull=False)
            ),
        ]
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def clean(self):
        """Valida que los roles no-PA tengan un negocio asignado"""
        super().clean()
        if self.role != "PA" and not self.business:
            raise ValidationError({
                "business": "Este campo es obligatorio para roles que no sean Administrador de la plataforma."
            })
        if self.role == "PA" and self.business:
            raise ValidationError({
                "business": "Los Administradores de la plataforma no deben estar asociados a un negocio."
            })

    def save(self, *args, **kwargs):
        """Asegura que la validación se ejecute"""
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def is_platform_admin(self):
        """Retorna True si el usuario es administrador de la plataforma"""
        return self.role == "PA"

    def __str__(self):
        business_name = self.business.name if self.business else "Plataforma"
        return f"{self.user.get_full_name() or self.user.username} - {business_name} ({self.get_role_display()})"


class Order(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # document = models.ForeignKey(SunatRecord, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)