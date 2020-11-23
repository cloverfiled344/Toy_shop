from django.db import models
from django.urls import reverse


# Create your models here.
# # user_name : toy_shop ,  password: toy_shop1234


class Category(models.Model):

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        ordering = ('name', )
        verbose_name = 'product'
        verbose_name_plural = 'products'

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    
class Cart(models.Model):

    class Meta:
        ordering = ['date_added']
        db_table = 'Cart'

    cart_id = models.CharField(max_length=255, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):

    class Meta:
        db_table = 'CartItem'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product