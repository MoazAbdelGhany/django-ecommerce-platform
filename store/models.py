from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_category_url(self):
        return reverse('store:products_by_category' , args=[self.slug])


class Product(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AV", "Available"
        DRAFT = "DF", "Draft"

    category = models.ForeignKey(Category , on_delete= models.CASCADE , related_name= 'products')
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="products/images/")
    description = models.TextField(max_length=1500)
    price = models.DecimalField(max_digits=9, decimal_places=2 , validators=[MinValueValidator(0)])
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.AVAILABLE
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created_at"]),
        ]

   
    def get_product_url(self):
        return reverse('store:product_details', args=[self.slug])