from rest_framework import viewsets,permissions
from .models import *
from .serialazers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .filter import *
from .permissions import CheckOwner
from rest_framework.response import Response


class ProductListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerialazer
    search_fields = ['product_name']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price', 'date']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class =ProductSerialazer
    search_fields = ['product_name']
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price','date']
    permission_classes = [CheckOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerialazer






class UserProfileViewSet(viewsets.ModelViewSet):
    queryset =  UserProfile.objects.all()
    serializer_class = UserProfileSerialazer





class ProductPhotoViewSet(viewsets.ModelViewSet):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerialazer

class RaitingViewSet(viewsets.ModelViewSet):
    queryset = Raiting.objects.all()
    serializer_class = RaitingSerialazer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Raiting.objects.all()
    serializer_class = ReviewSerialazer



class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerialazer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerialazer

    def get_queryset(self):
        return Cart.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)













