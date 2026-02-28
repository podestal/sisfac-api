from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Business(models.Model):
    """
    Issuer entity (RUC owner).
    MVP: keep simple but add constraints to avoid future pain.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    # If this business will issue electronic documents, it should have a RUC.
    ruc = models.CharField(max_length=11, null=True, blank=True, db_index=True)

    # ⚠️ If this is APISUNAT token, rename to apisunat_token later.
    # If this is actual SOL password, do NOT store it as plain text in production.
    sol_key = models.CharField(max_length=255, null=True, blank=True)

    tax_enabled = models.BooleanField(
        default=False,
        help_text="Si está activo, este negocio emite/recibe comprobantes SUNAT."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["ruc"])]

    def clean(self):
        super().clean()
        if self.tax_enabled:
            if not self.ruc:
                raise ValidationError({"ruc": "RUC es obligatorio si tax_enabled=True."})
            if len(self.ruc) != 11 or not self.ruc.isdigit():
                raise ValidationError({"ruc": "RUC debe tener 11 dígitos numéricos."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Category(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="categories")
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

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")

    code = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    stock = models.IntegerField(default=0)

    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)

    unit_of_measurement = models.CharField(choices=UNIT_OF_MEASUREMENT_CHOICES, max_length=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()
        if self.business_id and self.category_id:
            if self.category.business_id != self.business_id:
                raise ValidationError({"category": "This category belongs to a different business."})

    def save(self, *args, **kwargs):
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

    employee_id = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

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

    def clean(self):
        super().clean()
        if self.role != "PA" and not self.business:
            raise ValidationError({"business": "Este campo es obligatorio para roles que no sean Administrador de la plataforma."})
        if self.role == "PA" and self.business:
            raise ValidationError({"business": "Los Administradores de la plataforma no deben estar asociados a un negocio."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Order(models.Model):
    """
    Source of truth for sales in your system.
    Taxes module can generate a SUNAT document from an Order.
    """
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="orders")

    STATUS_CHOICES = [
        ("OPEN", "Abierto"),
        ("PAID", "Pagado"),
        ("CANCELLED", "Cancelado"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")

    # Minimal payment info (helps accounting and SUNAT selection)
    PAYMENT_TERM_CHOICES = [("CASH", "Contado"), ("CREDIT", "Crédito")]
    payment_term = models.CharField(max_length=10, choices=PAYMENT_TERM_CHOICES, default="CASH")

    CURRENCY_CHOICES = [("PEN", "Soles"), ("USD", "Dólares")]
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PEN")

    issued_at = models.DateTimeField(null=True, blank=True, help_text="Cuando se emitió el comprobante (si aplica)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")

    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)