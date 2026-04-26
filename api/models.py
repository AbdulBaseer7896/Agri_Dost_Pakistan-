from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Category for products (e.g., Seeds, Fertilizers, Pesticides)"""
    name_en = models.CharField(max_length=100)
    name_ur = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="React icon name (optional)")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name_en']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name_en


class Product(models.Model):
    """Agriculture product"""
    name_en = models.CharField(max_length=200)
    name_ur = models.CharField(max_length=200)
    description_en = models.TextField()
    description_ur = models.TextField()
    short_description_en = models.CharField(max_length=300, blank=True)
    short_description_ur = models.CharField(max_length=300, blank=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unit_en = models.CharField(max_length=50, default='per kg', help_text="e.g., per kg, per bag, per litre")
    unit_ur = models.CharField(max_length=50, default='فی کلو')

    stock = models.IntegerField(default=0)
    is_in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True)
    video = models.FileField(upload_to='products/videos/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name_en

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    @property
    def discount_percent(self):
        if self.has_discount:
            return round(((self.price - self.discount_price) / self.price) * 100)
        return 0


class ProductImage(models.Model):
    """Multiple images for a product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for {self.product.name_en}"


class Order(models.Model):
    """Order placed by a customer through the form"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('contacted', 'Contacted'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Sale Completed'),
        ('not_interested', 'Not Interested'),
        ('cancelled', 'Cancelled'),
    ]

    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='orders')
    product_name_snapshot = models.CharField(max_length=200, blank=True, help_text="Product name at time of order")
    quantity = models.IntegerField(default=1)
    notes = models.TextField(blank=True)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes by admin")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.product and not self.product_name_snapshot:
            self.product_name_snapshot = self.product.name_en
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class Testimonial(models.Model):
    """Customer testimonial videos for landing page"""
    customer_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    title_en = models.CharField(max_length=200, blank=True)
    title_ur = models.CharField(max_length=200, blank=True)
    description_en = models.TextField(blank=True)
    description_ur = models.TextField(blank=True)
    video = models.FileField(upload_to='testimonials/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='testimonials/thumbnails/', blank=True, null=True)
    rating = models.IntegerField(default=5, help_text="1 to 5")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.title_en}"


class HeroBanner(models.Model):
    """Hero banner images for the landing page"""
    title_en = models.CharField(max_length=200, blank=True)
    title_ur = models.CharField(max_length=200, blank=True)
    subtitle_en = models.CharField(max_length=300, blank=True)
    subtitle_ur = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title_en or f"Banner {self.id}"


class SiteSettings(models.Model):
    """Singleton model for site-wide settings"""
    whatsapp_number = models.CharField(max_length=20, default='+923001234567', help_text="Format: +923001234567")
    contact_phone = models.CharField(max_length=20, default='+923001234567')
    contact_email = models.EmailField(default='info@agridost.pk')
    address_en = models.TextField(blank=True, default='Lahore, Pakistan')
    address_ur = models.TextField(blank=True, default='لاہور، پاکستان')
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    about_en = models.TextField(blank=True, default='We are committed to providing high-quality agriculture products to farmers across Pakistan.')
    about_ur = models.TextField(blank=True, default='ہم پاکستان بھر کے کسانوں کو اعلیٰ معیار کی زرعی مصنوعات فراہم کرنے کے لیے پرعزم ہیں۔')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Site Settings'
