from django.db import models

# ===========================
# Tables supplémentaires demandées
# ===========================

class Capacity(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    label = models.CharField(max_length=255, db_column='label')

    class Meta:
        db_table = 'capacity'

    def __str__(self):
        return self.label


class UnitOfMeasure(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    label = models.CharField(max_length=255, db_column='label')

    class Meta:
        db_table = 'unit_of_measure'

    def __str__(self):
        return self.label


class TaxeRate(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    label = models.CharField(max_length=255, db_column='label')
    value = models.DecimalField(max_digits=5, decimal_places=2, db_column='value')

    class Meta:
        db_table = 'taxe_rate'

    def __str__(self):
        return f"{self.label} ({self.value}%)"


# ===========================
# Tables existantes avec mises à jour
# ===========================

class ProductState(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    state_label = models.CharField(max_length=255, db_column='label')

    class Meta:
        db_table = 'product_state'

    def __str__(self):
        return self.state_label


class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    category_name = models.CharField(max_length=255, db_column='label')

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.category_name


class Store(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    store_label = models.CharField(max_length=127, db_column='label')
    address = models.CharField(max_length=255, db_column='address')
    postal_code = models.CharField(max_length=10, db_column='postal_code')
    city = models.CharField(max_length=50, db_column='city')
    country = models.CharField(max_length=255, db_column='country', default='France')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, db_column='longitude', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, db_column='latitude', null=True, blank=True)
    store_creation_date = models.DateTimeField(auto_now_add=True, db_column='create_date')
    store_modification_date = models.DateTimeField(auto_now=True, db_column='update_date')

    class Meta:
        db_table = 'store'

    def __str__(self):
        return self.store_label


class Product(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    product_label = models.CharField(max_length=255, db_column='product_label')
    ticket_label = models.CharField(max_length=255, db_column='ticket_label', null=True, blank=True)
    barcode = models.CharField(max_length=255, db_column='barcode')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_category'
    )
    image = models.CharField(max_length=255, db_column='image', null=True, blank=True)
    state = models.ForeignKey(
        ProductState,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_state'
    )
    generic_label_id = models.CharField(max_length=255, db_column='generic_label_id', null=True, blank=True)
    capacity = models.ForeignKey(
        Capacity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_capacity'
    )
    unit_of_measure = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='uom_id'
    )
    product_creation_date = models.DateTimeField(auto_now_add=True, db_column='product_creation_date')
    product_modification_date = models.DateTimeField(auto_now=True, db_column='product_modification_date')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.product_label


class RelStorePrice(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column='id_product'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        db_column='id_store'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='price')
    price_exclude = models.DecimalField(max_digits=10, decimal_places=2, db_column='price_exclude', null=True, blank=True)
    taxe_rate = models.ForeignKey(
        TaxeRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='taxe_rate_id'
    )
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, db_column='discounted_price', null=True, blank=True)
    is_discount = models.BooleanField(default=False, db_column='is_discount')
    proof = models.CharField(max_length=255, db_column='proof', null=True, blank=True)
    price_creation_date = models.DateTimeField(auto_now_add=True, db_column='create_date')
    price_modification_date = models.DateTimeField(auto_now=True, db_column='update_date')

    class Meta:
        db_table = 'rel_store_price'

    def __str__(self):
        return f"Price for product {self.product} in store {self.store}"