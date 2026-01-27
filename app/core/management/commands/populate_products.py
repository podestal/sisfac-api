"""
Django management command to populate products for a Home Depot-like store.
Creates 5 products per category in Spanish.
"""
from django.core.management.base import BaseCommand
from operations.models import Business, Category, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Popula productos para una tienda tipo Home Depot (5 por categoría, en español)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--business-id',
            type=int,
            help='ID del negocio del cual se crearán los productos',
        )
        parser.add_argument(
            '--business-name',
            type=str,
            help='Nombre del negocio del cual se crearán los productos',
        )
        parser.add_argument(
            '--category-id',
            type=int,
            help='ID de la categoría específica (si no se especifica, usa todas)',
        )

    def handle(self, *args, **options):
        business_id = options.get('business_id')
        business_name = options.get('business_name')
        category_id = options.get('category_id')

        # Obtener el negocio
        if business_id:
            try:
                business = Business.objects.get(id=business_id)
            except Business.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'No se encontró un negocio con ID {business_id}')
                )
                return
        elif business_name:
            try:
                business = Business.objects.get(name=business_name)
            except Business.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'No se encontró un negocio con nombre "{business_name}"')
                )
                return
        else:
            business = Business.objects.first()
            if not business:
                self.stdout.write(
                    self.style.ERROR('No se encontró ningún negocio. Crea uno primero.')
                )
                return

        # Obtener categorías
        if category_id:
            try:
                categories = [Category.objects.get(id=category_id, business=business)]
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'No se encontró una categoría con ID {category_id} para este negocio')
                )
                return
        else:
            categories = Category.objects.filter(business=business)
            if not categories.exists():
                self.stdout.write(
                    self.style.ERROR('No se encontraron categorías para este negocio. Crea categorías primero.')
                )
                return

        # Definir productos por categoría
        products_by_category = {
            'Herramientas': [
                {'name': 'Martillo de Carpintero 16 oz', 'code': 'HERR-001', 'unit': 'U', 'buy': 25.00, 'sell': 35.00, 'stock': 50},
                {'name': 'Taladro Eléctrico Inalámbrico', 'code': 'HERR-002', 'unit': 'U', 'buy': 180.00, 'sell': 250.00, 'stock': 20},
                {'name': 'Destornillador Phillips #2', 'code': 'HERR-003', 'unit': 'U', 'buy': 8.00, 'sell': 12.00, 'stock': 100},
                {'name': 'Llave Inglesa Ajustable 8"', 'code': 'HERR-004', 'unit': 'U', 'buy': 35.00, 'sell': 48.00, 'stock': 40},
                {'name': 'Sierra Circular Manual', 'code': 'HERR-005', 'unit': 'U', 'buy': 45.00, 'sell': 65.00, 'stock': 30},
            ],
            'Pinturas y Accesorios': [
                {'name': 'Pintura Látex Interior Blanca 1 Galón', 'code': 'PINT-001', 'unit': 'L', 'buy': 45.00, 'sell': 65.00, 'stock': 80},
                {'name': 'Brocha de Cerdas Naturales 4"', 'code': 'PINT-002', 'unit': 'U', 'buy': 12.00, 'sell': 18.00, 'stock': 60},
                {'name': 'Rodillo de Espuma 9"', 'code': 'PINT-003', 'unit': 'U', 'buy': 8.00, 'sell': 15.00, 'stock': 70},
                {'name': 'Cinta de Enmascarar 2" x 50m', 'code': 'PINT-004', 'unit': 'U', 'buy': 5.00, 'sell': 9.00, 'stock': 120},
                {'name': 'Laca Acrílica Transparente 1L', 'code': 'PINT-005', 'unit': 'L', 'buy': 28.00, 'sell': 42.00, 'stock': 50},
            ],
            'Plomería': [
                {'name': 'Tubería PVC 1/2" x 3m', 'code': 'PLOM-001', 'unit': 'U', 'buy': 15.00, 'sell': 22.00, 'stock': 100},
                {'name': 'Grifo Monomando para Cocina', 'code': 'PLOM-002', 'unit': 'U', 'buy': 85.00, 'sell': 125.00, 'stock': 25},
                {'name': 'Inodoro Completo Estándar', 'code': 'PLOM-003', 'unit': 'U', 'buy': 180.00, 'sell': 280.00, 'stock': 15},
                {'name': 'Llave de Paso 1/2"', 'code': 'PLOM-004', 'unit': 'U', 'buy': 12.00, 'sell': 20.00, 'stock': 80},
                {'name': 'Codo PVC 90° 1/2"', 'code': 'PLOM-005', 'unit': 'U', 'buy': 3.00, 'sell': 5.00, 'stock': 200},
            ],
            'Electricidad': [
                {'name': 'Cable Eléctrico THWN #12 x 100m', 'code': 'ELEC-001', 'unit': 'U', 'buy': 120.00, 'sell': 180.00, 'stock': 30},
                {'name': 'Interruptor Simple 15A', 'code': 'ELEC-002', 'unit': 'U', 'buy': 8.00, 'sell': 15.00, 'stock': 150},
                {'name': 'Toma de Corriente Doble 20A', 'code': 'ELEC-003', 'unit': 'U', 'buy': 12.00, 'sell': 22.00, 'stock': 100},
                {'name': 'Foco LED 12W E27', 'code': 'ELEC-004', 'unit': 'U', 'buy': 6.00, 'sell': 12.00, 'stock': 200},
                {'name': 'Caja Eléctrica Metálica 4x4"', 'code': 'ELEC-005', 'unit': 'U', 'buy': 15.00, 'sell': 25.00, 'stock': 80},
            ],
            'Jardín y Exterior': [
                {'name': 'Manguera de Jardín 1/2" x 15m', 'code': 'JARD-001', 'unit': 'U', 'buy': 35.00, 'sell': 55.00, 'stock': 40},
                {'name': 'Pala de Jardín con Mango', 'code': 'JARD-002', 'unit': 'U', 'buy': 25.00, 'sell': 38.00, 'stock': 30},
                {'name': 'Semillas de Tomate 50g', 'code': 'JARD-003', 'unit': 'G', 'buy': 8.00, 'sell': 15.00, 'stock': 50},
                {'name': 'Fertilizante Universal 5kg', 'code': 'JARD-004', 'unit': 'KG', 'buy': 45.00, 'sell': 70.00, 'stock': 25},
                {'name': 'Maceta de Plástico 30cm', 'code': 'JARD-005', 'unit': 'U', 'buy': 12.00, 'sell': 20.00, 'stock': 60},
            ],
            'Construcción': [
                {'name': 'Cemento Portland 50kg', 'code': 'CONS-001', 'unit': 'KG', 'buy': 18.00, 'sell': 28.00, 'stock': 100},
                {'name': 'Ladrillo King Kong 18 huecos', 'code': 'CONS-002', 'unit': 'U', 'buy': 0.45, 'sell': 0.75, 'stock': 5000},
                {'name': 'Arena Gruesa 1m³', 'code': 'CONS-003', 'unit': 'U', 'buy': 120.00, 'sell': 180.00, 'stock': 20},
                {'name': 'Varilla de Acero #4 x 9m', 'code': 'CONS-004', 'unit': 'U', 'buy': 35.00, 'sell': 55.00, 'stock': 80},
                {'name': 'Alambre N°16 x 50kg', 'code': 'CONS-005', 'unit': 'KG', 'buy': 8.00, 'sell': 14.00, 'stock': 200},
            ],
            'Pisos y Revestimientos': [
                {'name': 'Cerámico 30x30cm Caja 1.5m²', 'code': 'PISO-001', 'unit': 'BX', 'buy': 45.00, 'sell': 75.00, 'stock': 50},
                {'name': 'Piso Laminado 15mm x 2m²', 'code': 'PISO-002', 'unit': 'BX', 'buy': 65.00, 'sell': 95.00, 'stock': 40},
                {'name': 'Alfombra Sintética 2x3m', 'code': 'PISO-003', 'unit': 'U', 'buy': 85.00, 'sell': 130.00, 'stock': 20},
                {'name': 'Porcelanato 60x60cm Caja 1.44m²', 'code': 'PISO-004', 'unit': 'BX', 'buy': 120.00, 'sell': 180.00, 'stock': 30},
                {'name': 'Adhesivo para Cerámico 20kg', 'code': 'PISO-005', 'unit': 'KG', 'buy': 25.00, 'sell': 40.00, 'stock': 60},
            ],
            'Iluminación': [
                {'name': 'Lámpara Colgante Moderna', 'code': 'ILUM-001', 'unit': 'U', 'buy': 85.00, 'sell': 140.00, 'stock': 25},
                {'name': 'Foco LED 18W Dimmable', 'code': 'ILUM-002', 'unit': 'U', 'buy': 12.00, 'sell': 22.00, 'stock': 150},
                {'name': 'Lámpara de Mesa LED', 'code': 'ILUM-003', 'unit': 'U', 'buy': 45.00, 'sell': 75.00, 'stock': 30},
                {'name': 'Tira LED RGB 5m', 'code': 'ILUM-004', 'unit': 'U', 'buy': 35.00, 'sell': 60.00, 'stock': 40},
                {'name': 'Plafón LED 24W Redondo', 'code': 'ILUM-005', 'unit': 'U', 'buy': 55.00, 'sell': 90.00, 'stock': 35},
            ],
            'Cocina y Baño': [
                {'name': 'Grifo para Lavadero Monomando', 'code': 'COBA-001', 'unit': 'U', 'buy': 95.00, 'sell': 150.00, 'stock': 20},
                {'name': 'Espejo de Baño 60x80cm', 'code': 'COBA-002', 'unit': 'U', 'buy': 120.00, 'sell': 190.00, 'stock': 15},
                {'name': 'Organizador de Cocina 3 Niveles', 'code': 'COBA-003', 'unit': 'U', 'buy': 45.00, 'sell': 75.00, 'stock': 30},
                {'name': 'Toallero de Acero Inoxidable', 'code': 'COBA-004', 'unit': 'U', 'buy': 35.00, 'sell': 55.00, 'stock': 40},
                {'name': 'Fregadero de Acero Inoxidable', 'code': 'COBA-005', 'unit': 'U', 'buy': 180.00, 'sell': 280.00, 'stock': 12},
            ],
            'Seguridad y Cerraduras': [
                {'name': 'Candado de Seguridad 40mm', 'code': 'SEGU-001', 'unit': 'U', 'buy': 25.00, 'sell': 40.00, 'stock': 60},
                {'name': 'Cerradura de Pomo Simple', 'code': 'SEGU-002', 'unit': 'U', 'buy': 35.00, 'sell': 55.00, 'stock': 50},
                {'name': 'Cerradura de Seguridad Multipunto', 'code': 'SEGU-003', 'unit': 'U', 'buy': 85.00, 'sell': 140.00, 'stock': 25},
                {'name': 'Candado de Cadena 1m', 'code': 'SEGU-004', 'unit': 'U', 'buy': 45.00, 'sell': 70.00, 'stock': 30},
                {'name': 'Alarma de Puerta Inalámbrica', 'code': 'SEGU-005', 'unit': 'U', 'buy': 65.00, 'sell': 100.00, 'stock': 20},
            ],
            'Climatización': [
                {'name': 'Ventilador de Techo 56"', 'code': 'CLIM-001', 'unit': 'U', 'buy': 180.00, 'sell': 280.00, 'stock': 15},
                {'name': 'Ventilador de Pie 18"', 'code': 'CLIM-002', 'unit': 'U', 'buy': 85.00, 'sell': 140.00, 'stock': 25},
                {'name': 'Calefactor Eléctrico 2000W', 'code': 'CLIM-003', 'unit': 'U', 'buy': 120.00, 'sell': 190.00, 'stock': 20},
                {'name': 'Aire Acondicionado Portátil 12000 BTU', 'code': 'CLIM-004', 'unit': 'U', 'buy': 850.00, 'sell': 1300.00, 'stock': 8},
                {'name': 'Termostato Digital Programable', 'code': 'CLIM-005', 'unit': 'U', 'buy': 95.00, 'sell': 150.00, 'stock': 18},
            ],
            'Organización y Almacenamiento': [
                {'name': 'Estantería Metálica 5 Niveles', 'code': 'ORGA-001', 'unit': 'U', 'buy': 120.00, 'sell': 190.00, 'stock': 20},
                {'name': 'Caja de Almacenamiento 60L', 'code': 'ORGA-002', 'unit': 'U', 'buy': 25.00, 'sell': 40.00, 'stock': 80},
                {'name': 'Organizador de Herramientas', 'code': 'ORGA-003', 'unit': 'U', 'buy': 45.00, 'sell': 75.00, 'stock': 35},
                {'name': 'Repisa Flotante 60cm', 'code': 'ORGA-004', 'unit': 'U', 'buy': 35.00, 'sell': 55.00, 'stock': 50},
                {'name': 'Cajonera de Plástico 3 Cajones', 'code': 'ORGA-005', 'unit': 'U', 'buy': 55.00, 'sell': 90.00, 'stock': 30},
            ],
            'Ferretería General': [
                {'name': 'Tornillos para Madera #8 x 2" Caja 100u', 'code': 'FERR-001', 'unit': 'BX', 'buy': 12.00, 'sell': 20.00, 'stock': 100},
                {'name': 'Clavos Galvanizados 2" x 1kg', 'code': 'FERR-002', 'unit': 'KG', 'buy': 8.00, 'sell': 14.00, 'stock': 150},
                {'name': 'Tuercas Hexagonales M8 x 50u', 'code': 'FERR-003', 'unit': 'BX', 'buy': 15.00, 'sell': 25.00, 'stock': 80},
                {'name': 'Pernos de Acero M10 x 10cm x 20u', 'code': 'FERR-004', 'unit': 'BX', 'buy': 18.00, 'sell': 30.00, 'stock': 60},
                {'name': 'Arandelas Planas M8 x 100u', 'code': 'FERR-005', 'unit': 'BX', 'buy': 10.00, 'sell': 18.00, 'stock': 120},
            ],
            'Madera y Tableros': [
                {'name': 'Tablero de MDF 18mm 1.22x2.44m', 'code': 'MADE-001', 'unit': 'U', 'buy': 85.00, 'sell': 140.00, 'stock': 25},
                {'name': 'Pino Cepillado 1"x4" x 2.44m', 'code': 'MADE-002', 'unit': 'U', 'buy': 35.00, 'sell': 55.00, 'stock': 60},
                {'name': 'Contrachapado 15mm 1.22x2.44m', 'code': 'MADE-003', 'unit': 'U', 'buy': 95.00, 'sell': 150.00, 'stock': 20},
                {'name': 'Aglomerado 18mm 1.22x2.44m', 'code': 'MADE-004', 'unit': 'U', 'buy': 65.00, 'sell': 100.00, 'stock': 30},
                {'name': 'Listón de Pino 2"x2" x 2.44m', 'code': 'MADE-005', 'unit': 'U', 'buy': 15.00, 'sell': 25.00, 'stock': 100},
            ],
            'Automotriz': [
                {'name': 'Aceite de Motor 15W40 5L', 'code': 'AUTO-001', 'unit': 'L', 'buy': 45.00, 'sell': 70.00, 'stock': 40},
                {'name': 'Filtro de Aceite Universal', 'code': 'AUTO-002', 'unit': 'U', 'buy': 18.00, 'sell': 30.00, 'stock': 50},
                {'name': 'Batería de Auto 12V 60Ah', 'code': 'AUTO-003', 'unit': 'U', 'buy': 280.00, 'sell': 420.00, 'stock': 12},
                {'name': 'Llanta de Repuesto 185/65R15', 'code': 'AUTO-004', 'unit': 'U', 'buy': 180.00, 'sell': 280.00, 'stock': 15},
                {'name': 'Gato Hidráulico 2 Toneladas', 'code': 'AUTO-005', 'unit': 'U', 'buy': 95.00, 'sell': 150.00, 'stock': 20},
            ],
        }

        total_created = 0
        total_skipped = 0

        for category in categories:
            category_name = category.name
            products_data = products_by_category.get(category_name, [])

            if not products_data:
                self.stdout.write(
                    self.style.WARNING(f'⚠ No hay productos definidos para la categoría: {category_name}')
                )
                continue

            self.stdout.write(f'\n📦 Categoría: {category_name}')
            created_in_category = 0
            skipped_in_category = 0

            for prod_data in products_data:
                product, created = Product.objects.get_or_create(
                    business=business,
                    category=category,
                    code=prod_data['code'],
                    defaults={
                        'name': prod_data['name'],
                        'description': f'Producto de la categoría {category_name}',
                        'stock': prod_data['stock'],
                        'sell_price': Decimal(str(prod_data['sell'])),
                        'unit_of_measurement': prod_data['unit'],
                        'buy_price': Decimal(str(prod_data['buy'])),
                    }
                )

                if created:
                    created_in_category += 1
                    total_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ {prod_data["name"]}')
                    )
                else:
                    skipped_in_category += 1
                    total_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(f'  ⊘ {prod_data["name"]} (ya existe)')
                    )

            self.stdout.write(
                f'  → Creados: {created_in_category} | Existentes: {skipped_in_category}'
            )

        # Resumen final
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Proceso completado!\n'
                f'   Negocio: {business.name}\n'
                f'   Categorías procesadas: {categories.count()}\n'
                f'   Productos creados: {total_created}\n'
                f'   Productos existentes: {total_skipped}\n'
                f'   Total de productos: {Product.objects.filter(business=business).count()}'
            )
        )
