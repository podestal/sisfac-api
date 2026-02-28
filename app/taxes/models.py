# taxes/models.py
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from operations.models import Business, Order, Product


class BusinessSunatConfig(models.Model):
    """
    APISUNAT config per Business.
    APISUNAT uses personaId + personaToken.
    """
    business = models.OneToOneField(Business, on_delete=models.CASCADE, related_name="sunat_config")

    persona_id = models.CharField(max_length=100)
    persona_token = models.CharField(max_length=200)

    production_enabled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Party(models.Model):
    """
    Customer/Supplier data needed for SUNAT docs.
    Scoped per Business.
    """
    DOC_TYPE_CHOICES = [
        ("0", "SIN DOC"),
        ("1", "DNI"),
        ("4", "CE"),
        ("6", "RUC"),
        ("7", "PASAPORTE"),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="parties")

    doc_type = models.CharField(max_length=2, choices=DOC_TYPE_CHOICES)
    doc_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, default="")

    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")

    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["business", "doc_type", "doc_number"])]
        constraints = [
            models.UniqueConstraint(
                fields=["business", "doc_type", "doc_number"],
                name="uq_party_business_doctype_docnumber",
            )
        ]


class DocumentType(models.Model):
    """
    SUNAT doc types.
    01 Factura, 03 Boleta, 07 Nota de crédito, 08 Nota de débito.
    """
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class SunatDocument(models.Model):
    """
    Business comprobante to be sent to SUNAT (via APISUNAT).
    """
    DIRECTION_CHOICES = [("SALE", "Venta"), ("PURCHASE", "Compra")]  # purchases later
    STATUS_CHOICES = [("DRAFT", "Borrador"), ("ISSUED", "Emitido"), ("VOID", "Anulado")]

    CURRENCY_CHOICES = [("PEN", "Soles"), ("USD", "Dólares")]
    PAYMENT_TERM_CHOICES = [("CASH", "Contado"), ("CREDIT", "Crédito")]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="sunat_documents")
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES, default="SALE")

    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, related_name="documents")
    series = models.CharField(max_length=10)
    number = models.PositiveIntegerField()

    issue_date = models.DateField()

    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="documents")

    # Optional link to Order (recommended MVP path)
    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sunat_document",
        help_text="Si el comprobante se generó desde un pedido."
    )

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PEN")
    exchange_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )

    payment_term = models.CharField(max_length=10, choices=PAYMENT_TERM_CHOICES, default="CASH")
    due_date = models.DateField(null=True, blank=True)

    # Totals (MVP: taxable + igv + total)
    total_taxable = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_igv = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="DRAFT")

    # For NC/ND later
    ref_document = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="referenced_by",
    )

    class Meta:
        indexes = [
            models.Index(fields=["business", "issue_date"]),
            models.Index(fields=["business", "document_type", "series", "number"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["business", "direction", "document_type", "series", "number"],
                name="uq_sunatdoc_business_dir_type_series_number",
            )
        ]

    def __str__(self) -> str:
        return f"{self.business.ruc}-{self.document_type.code}-{self.series}-{self.number}"


class SunatDocumentItem(models.Model):
    """
    Items for SUNAT doc. Link to Product optional but nice for traceability.
    """
    TAX_AFFECTATION_CHOICES = [
        ("10", "Gravado - Operación Onerosa (IGV)"),
        ("20", "Exonerado"),
        ("30", "Inafecto"),
        ("21", "Gratuito (referencial)"),
    ]

    document = models.ForeignKey(SunatDocument, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(Product, on_delete=models.PROTECT, null=True, blank=True, related_name="sunat_items")

    description = models.CharField(max_length=255)

    quantity = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal("1.0000"),
        validators=[MinValueValidator(Decimal("0.0001"))]
    )
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=4, default=Decimal("0.0000"),
        validators=[MinValueValidator(Decimal("0.0000"))]
    )
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    tax_affectation = models.CharField(max_length=2, choices=TAX_AFFECTATION_CHOICES, default="10")
    igv_rate = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal("0.1800"))

    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))


class SunatSubmission(models.Model):
    """
    One attempt to send to APISUNAT (sendBill) + final result (getById).
    Allows retries: many submissions per SunatDocument.
    """
    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("ACCEPTED", "Aceptado"),
        ("REJECTED", "Rechazado"),
        ("EXCEPTION", "Excepción"),
        ("ERROR", "Error interno"),
    ]

    document = models.ForeignKey(SunatDocument, on_delete=models.CASCADE, related_name="submissions")

    production = models.BooleanField(default=False)

    file_name = models.CharField(
        max_length=80,
        help_text="Formato típico: RUC-TIPO-SERIE-NUMERO"
    )

    apisunat_document_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="PENDING")

    xml_url = models.URLField(max_length=500, null=True, blank=True)
    cdr_url = models.URLField(max_length=500, null=True, blank=True)

    sunat_issued_at = models.DateTimeField(null=True, blank=True)
    sunat_responded_at = models.DateTimeField(null=True, blank=True)

    faults = models.JSONField(null=True, blank=True)
    notes = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    raw_request = models.JSONField(null=True, blank=True)
    raw_response = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)