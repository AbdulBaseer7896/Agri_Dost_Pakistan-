from rest_framework import serializers
from .models import (
    Category, Product, ProductImage, Order, Testimonial, HeroBanner, SiteSettings
)


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name_en', 'name_ur', 'icon', 'image', 'order', 'is_active', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)
    category_name_ur = serializers.CharField(source='category.name_ur', read_only=True)
    has_discount = serializers.BooleanField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ur', 'short_description_en', 'short_description_ur',
            'price', 'discount_price', 'final_price', 'has_discount', 'discount_percent',
            'unit_en', 'unit_ur', 'main_image', 'is_in_stock', 'is_featured',
            'category', 'category_name_en', 'category_name_ur', 'created_at'
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for detail views"""
    images = ProductImageSerializer(many=True, read_only=True)
    category_name_en = serializers.CharField(source='category.name_en', read_only=True)
    category_name_ur = serializers.CharField(source='category.name_ur', read_only=True)
    has_discount = serializers.BooleanField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ur', 'description_en', 'description_ur',
            'short_description_en', 'short_description_ur',
            'price', 'discount_price', 'final_price', 'has_discount', 'discount_percent',
            'unit_en', 'unit_ur', 'stock', 'is_in_stock', 'is_featured', 'is_active',
            'main_image', 'video', 'category', 'category_name_en', 'category_name_ur',
            'images', 'created_at', 'updated_at'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """For admin: create/update products"""
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name_en', 'name_ur', 'description_en', 'description_ur',
            'short_description_en', 'short_description_ur',
            'price', 'discount_price', 'unit_en', 'unit_ur',
            'stock', 'is_in_stock', 'is_featured', 'is_active',
            'main_image', 'video', 'category', 'uploaded_images'
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        for idx, image in enumerate(uploaded_images):
            ProductImage.objects.create(product=product, image=image, order=idx)
        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if uploaded_images:
            existing = instance.images.count()
            for idx, image in enumerate(uploaded_images):
                ProductImage.objects.create(product=instance, image=image, order=existing + idx)
        return instance


class OrderSerializer(serializers.ModelSerializer):
    product_name_en = serializers.CharField(source='product.name_en', read_only=True)
    product_name_ur = serializers.CharField(source='product.name_ur', read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'phone', 'address', 'city',
            'product', 'product_name_snapshot', 'product_name_en', 'product_name_ur',
            'product_image', 'quantity', 'notes', 'status', 'admin_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['admin_notes', 'status']


class OrderUpdateSerializer(serializers.ModelSerializer):
    """For admin to update order status"""
    class Meta:
        model = Order
        fields = ['status', 'admin_notes']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id', 'customer_name', 'location', 'title_en', 'title_ur',
            'description_en', 'description_ur', 'video', 'thumbnail',
            'rating', 'order', 'is_active', 'created_at'
        ]


class HeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBanner
        fields = [
            'id', 'title_en', 'title_ur', 'subtitle_en', 'subtitle_ur',
            'banner_type', 'image', 'video',
            'button_text_en', 'button_text_ur', 'button_link',
            'order', 'is_active', 'created_at'
        ]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'
