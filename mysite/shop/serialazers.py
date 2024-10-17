from rest_framework import serializers
from .models import *


class CategorySerialazer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class UserProfileSerialazer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileSimpleSerialazer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['name', 'last_name']




class RaitingSerialazer(serializers.ModelSerializer):
    user = UserProfileSimpleSerialazer()
    class Meta:
        model = Raiting
        fields = ['user','stars']




class ProductPhotoSerialazer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['image']




class ReviewSerialazer(serializers.ModelSerializer):
    author = UserProfileSimpleSerialazer()
    class Meta:
        model = Reveiw
        fields = ['id','author', 'parent_review','text']


class ProductListSerialazer(serializers.ModelSerializer):
    product = ProductPhotoSerialazer(read_only=True, many=True)
    category = CategorySerialazer()
    owner = UserProfileSimpleSerialazer()
    date_created = serializers.DateTimeField(format='%d-%m-%Y')

    class Meta:
        model = Product
        fields = ['id','product_name','price','category','product', 'date_created','owner','raitings']


class ProductSerialazer(serializers.ModelSerializer):
    category = CategorySerialazer()
    raitings = RaitingSerialazer(read_only=True,many=True)
    reviews = ReviewSerialazer(read_only=True,many=True)
    product = ProductPhotoSerialazer(read_only=True,many=True)
    date_created = serializers.DateTimeField('%d-%m-%Y')
    average_raitings = serializers.SerializerMethodField()
    owner = UserProfileSimpleSerialazer()

    class Meta:
        model = Product
        fields = ['id','product_name','category','description','product','video','price','activite',
                  'raitings','reviews','average_raitings','date_created','owner']

    def get_average_raitings(self,obj):
        return obj.get_average_raitings()


class CartItemSerialazer(serializers.ModelSerializer):
    product = ProductSerialazer(many=True,read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),write_only=True,source='product')

    class Meta:
        model = CarItem
        fields = ['id','product','product_id','quantity','get_total_price']


class CartSerialazer(serializers.ModelSerializer):
    items = CartItemSerialazer(read_only=True,many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id','user','items','total_price']

        def get_total_price(self,obj):
            return obj.get_total_price()


















