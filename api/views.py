from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q, Count

from .models import (
    Category, Product, ProductImage, Order, Testimonial, HeroBanner, SiteSettings
)
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer, ProductImageSerializer,
    OrderSerializer, OrderUpdateSerializer,
    TestimonialSerializer, HeroBannerSerializer, SiteSettingsSerializer
)


# ============== AUTH VIEWS ==============
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """Admin login endpoint - returns JWT tokens"""
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_staff:
        return Response(
            {'error': 'You do not have admin access'},
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff,
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_me(request):
    """Get current admin user info"""
    user = request.user
    if not user.is_staff:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
    })


# ============== CATEGORY VIEWS ==============
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Category.objects.all()
        if self.action == 'list' and not self.request.user.is_staff:
            qs = qs.filter(is_active=True)
        return qs.annotate(product_count=Count('products', filter=Q(products__is_active=True)))


# ============== PRODUCT VIEWS ==============
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name_en', 'name_ur', 'description_en', 'description_ur']
    ordering_fields = ['created_at', 'price', 'name_en']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'featured']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Product.objects.all().select_related('category').prefetch_related('images')
        # Public users see only active products
        if self.request.user.is_anonymous or not self.request.user.is_staff:
            qs = qs.filter(is_active=True)

        # Filtering
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category_id=category)

        is_featured = self.request.query_params.get('is_featured')
        if is_featured == 'true':
            qs = qs.filter(is_featured=True)

        return qs

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products for landing page"""
        products = self.get_queryset().filter(is_featured=True, is_active=True)[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['delete'], url_path='images/(?P<image_id>[^/.]+)', permission_classes=[IsAdminUser])
    def delete_image(self, request, pk=None, image_id=None):
        """Delete a product image"""
        try:
            image = ProductImage.objects.get(id=image_id, product_id=pk)
            image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)


# ============== ORDER VIEWS ==============
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        qs = Order.objects.all().select_related('product')
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(customer_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(address__icontains=search)
            )
        return qs

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def stats(self, request):
        """Get order statistics for the admin dashboard"""
        total = Order.objects.count()
        pending = Order.objects.filter(status='pending').count()
        completed = Order.objects.filter(status='completed').count()
        contacted = Order.objects.filter(status='contacted').count()
        not_interested = Order.objects.filter(status='not_interested').count()
        return Response({
            'total': total,
            'pending': pending,
            'contacted': contacted,
            'completed': completed,
            'not_interested': not_interested,
        })


# ============== TESTIMONIAL VIEWS ==============
class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = Testimonial.objects.all()
        if self.request.user.is_anonymous or not self.request.user.is_staff:
            qs = qs.filter(is_active=True)
        return qs


# ============== BANNER VIEWS ==============
class HeroBannerViewSet(viewsets.ModelViewSet):
    queryset = HeroBanner.objects.all()
    serializer_class = HeroBannerSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_queryset(self):
        qs = HeroBanner.objects.all()
        if self.request.user.is_anonymous or not self.request.user.is_staff:
            qs = qs.filter(is_active=True)
        return qs


# ============== SITE SETTINGS ==============
@api_view(['GET'])
@permission_classes([AllowAny])
def get_site_settings(request):
    """Public endpoint to get site settings (whatsapp number, contact info, etc.)"""
    settings_obj = SiteSettings.get_settings()
    serializer = SiteSettingsSerializer(settings_obj)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_site_settings(request):
    """Admin endpoint to update site settings"""
    settings_obj = SiteSettings.get_settings()
    serializer = SiteSettingsSerializer(settings_obj, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
