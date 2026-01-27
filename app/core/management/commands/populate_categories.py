"""
Django management command to populate categories for a Home Depot-like store.
Categories are in Spanish.
"""
from django.core.management.base import BaseCommand
from operations.models import Business, Category


class Command(BaseCommand):
    help = 'Popula categorías para una tienda tipo Home Depot (en español)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--business-id',
            type=int,
            help='ID del negocio al que se asociarán las categorías',
        )
        parser.add_argument(
            '--business-name',
            type=str,
            help='Nombre del negocio al que se asociarán las categorías',
        )

    def handle(self, *args, **options):
        business_id = options.get('business_id')
        business_name = options.get('business_name')

        # Obtener o crear el negocio
        if business_id:
            try:
                business = Business.objects.get(id=business_id)
            except Business.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'No se encontró un negocio con ID {business_id}')
                )
                return
        elif business_name:
            business, created = Business.objects.get_or_create(
                name=business_name,
                defaults={
                    'description': f'Negocio de ferretería y mejoras para el hogar: {business_name}'
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Negocio "{business_name}" creado exitosamente')
                )
        else:
            # Si no se especifica, usar el primer negocio o crear uno por defecto
            business = Business.objects.first()
            if not business:
                business = Business.objects.create(
                    name='Ferretería y Mejoras del Hogar',
                    description='Tienda de ferretería y mejoras para el hogar'
                )
                self.stdout.write(
                    self.style.SUCCESS('Se creó un negocio por defecto')
                )

        # Definir categorías tipo Home Depot en español
        categories_data = [
            {
                'name': 'Herramientas',
                'description': 'Herramientas manuales y eléctricas para construcción y reparación'
            },
            {
                'name': 'Pinturas y Accesorios',
                'description': 'Pinturas, brochas, rodillos y accesorios para pintura'
            },
            {
                'name': 'Plomería',
                'description': 'Tuberías, grifos, sanitarios y accesorios de plomería'
            },
            {
                'name': 'Electricidad',
                'description': 'Cables, interruptores, tomas de corriente y accesorios eléctricos'
            },
            {
                'name': 'Jardín y Exterior',
                'description': 'Plantas, semillas, herramientas de jardín y decoración exterior'
            },
            {
                'name': 'Construcción',
                'description': 'Materiales de construcción, cemento, ladrillos y estructuras'
            },
            {
                'name': 'Pisos y Revestimientos',
                'description': 'Pisos laminados, cerámicos, alfombras y revestimientos'
            },
            {
                'name': 'Iluminación',
                'description': 'Lámparas, focos, luces LED y accesorios de iluminación'
            },
            {
                'name': 'Cocina y Baño',
                'description': 'Muebles, accesorios y electrodomésticos para cocina y baño'
            },
            {
                'name': 'Seguridad y Cerraduras',
                'description': 'Cerraduras, candados, sistemas de seguridad y alarmas'
            },
            {
                'name': 'Climatización',
                'description': 'Ventiladores, calefactores, aires acondicionados y accesorios'
            },
            {
                'name': 'Organización y Almacenamiento',
                'description': 'Estanterías, organizadores, cajas de almacenamiento y repisas'
            },
            {
                'name': 'Ferretería General',
                'description': 'Tornillos, clavos, tuercas, pernos y elementos de fijación'
            },
            {
                'name': 'Madera y Tableros',
                'description': 'Maderas, tableros, aglomerados y materiales de carpintería'
            },
            {
                'name': 'Automotriz',
                'description': 'Herramientas y accesorios para vehículos y mantenimiento automotriz'
            },
        ]

        created_count = 0
        skipped_count = 0

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                business=business,
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Categoría creada: {cat_data["name"]}')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ Categoría ya existe: {cat_data["name"]}')
                )

        # Resumen
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado!\n'
                f'   Negocio: {business.name}\n'
                f'   Categorías creadas: {created_count}\n'
                f'   Categorías existentes: {skipped_count}\n'
                f'   Total de categorías: {Category.objects.filter(business=business).count()}'
            )
        )
