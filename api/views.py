# from django.http import JsonResponse
from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_headers
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import InStockFilterBackend, OrderFilter, ProductFilter
from api.models import Order, Product, User
from api.serializers import (OrderSerializer, ProductInfoSerializers,
                             ProductSerializer, OrderCreateSerializer, UserSerializer)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    # queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter 
    #alternative way to order and search
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend,
        ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    pagination_class.page_query_param = 'page_number'
    pagination_class.page_size_query_param = 'size'
    pagination_class.max_page_size = 4

    def create(self, request, *args, **kwargs):
        # print(request.data)
        return super().create(request, *args, **kwargs)
        
    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE' ]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]


    # @method_decorator(cache_page(60 * 15, key_prefix='order_list'))
    # @method_decorator(vary_on_headers("Authorization"))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    # This action will be redundent for this user_orders purpose after adding the get_queryset method 
    # @action(
    #         detail=False, 
    #         methods=['get'], 
    #         url_path='user-orders',
    #     )
    # def user_orders(self, request):
    #     orders = self.get_queryset().filter(user=request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)

 
class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializers({
            'products' : products,
            'count' : len(products),
            'max_price' : products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)




# Old Class Based Views
   
# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.filter(user=self.request.user)



# Function Based Views.

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serialzer = ProductSerializer(products, many=True)
#     return Response(serialzer.data)


# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serialzer = ProductSerializer(product)
#     return Response(serialzer.data)

# @api_view(['GET'])
# def order_list(request):
#     # orders = Order.objects.prefetch_related(
#     #     'items', 'items__product',
#     # ).all()
#     orders = Order.objects.prefetch_related('items__product') # Both are same. This is perfect. 

#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


# def product_list(request):
#     products = Product.objects.all()
#     serialzer = ProductSerializer(products, many=True)
#     return JsonResponse(
#         {
#             'data' : serialzer.data
#         }
#     )

# @api_view(['GET'])
# def product_info(request):
#     products = Product.objects.all()
#     serializer = ProductInfoSerializers({
#         'products' : products,
#         'count' : len(products),
#         'max_price' : products.aggregate(max_price=Max('price'))['max_price']
#     })
#     return Response(serializer.data)