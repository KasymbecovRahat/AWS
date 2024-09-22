from .models import Product
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    model = Product
    fields = ('product_name', 'description')