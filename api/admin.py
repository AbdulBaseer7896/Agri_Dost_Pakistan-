from django.contrib import admin
from .models import (
    Category, Product, ProductImage, Order, Testimonial, HeroBanner, SiteSettings
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_ur', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['name_en', 'name_ur']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'category', 'price', 'discount_price', 'is_in_stock', 'is_featured', 'is_active']
    list_editable = ['price', 'discount_price', 'is_in_stock', 'is_featured', 'is_active']
    list_filter = ['category', 'is_in_stock', 'is_featured', 'is_active']
    search_fields = ['name_en', 'name_ur']
    inlines = [ProductImageInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone', 'product', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['customer_name', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'location', 'rating', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['whatsapp_number', 'contact_phone', 'contact_email']

    def has_add_permission(self, request):
        # Only one instance allowed
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
