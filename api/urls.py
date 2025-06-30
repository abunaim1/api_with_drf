from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('orders/', views.OrderListAPIView.as_view()),
    path('user-orders/', views.UserOrderListAPIView.as_view(), name='user-orders'),

        # Optional UI: Documention of API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
