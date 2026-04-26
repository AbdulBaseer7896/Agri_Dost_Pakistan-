from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'testimonials', views.TestimonialViewSet, basename='testimonial')
router.register(r'banners', views.HeroBannerViewSet, basename='banner')

urlpatterns = [
    # Auth
    path('auth/login/', views.admin_login, name='admin-login'),
    path('auth/me/', views.admin_me, name='admin-me'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Site settings
    path('settings/', views.get_site_settings, name='site-settings'),
    path('settings/update/', views.update_site_settings, name='update-site-settings'),

    # ViewSets
    path('', include(router.urls)),
]
