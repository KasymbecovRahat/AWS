from django.db import models



class UserProfile(models.Model):
    name = models.CharField(max_length=50,null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    age = models.PositiveSmallIntegerField(default=0,null=True, blank=True)
    date_registred = models.DateField(auto_now=True , null=True,blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    STATUS_CHOICES = (
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('simple', 'Simple')

    )

    status = models.CharField(max_length=100 , choices=STATUS_CHOICES,default='simple')

    def __str__(self):
        return f'{self.name},{self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=30,null=True,blank=True)
    category = models.ForeignKey(Category,related_name='product',on_delete=models.CASCADE)
    description = models.TextField(null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()
    activite = models.BooleanField(verbose_name='в наличии',default=True )
    video = models.FileField(upload_to='video/',verbose_name='видео',null=True,blank=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    def get_average_raitings(self):
        raitings = self.raitings.all()
        if raitings.exists():
            return round(sum(rating.stars for rating in raitings) / raitings.count(),1)
        return 0


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, related_name='product',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image')


class Raiting(models.Model):
    product = models.ForeignKey(Product,related_name='raitings',on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,6)],verbose_name='Рейтинг')

    def __str__(self):
        return f'{self.product}-{self.user}-{self.stars}'


class Reveiw(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='reviews',on_delete=models.CASCADE)
    text = models.TextField()
    parent_review = models.ForeignKey('self',related_name='replice',null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}-{self.product}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE,related_name='cart')
    creat_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CarItem(models.Model):
    cart = models.ForeignKey(Cart,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

















