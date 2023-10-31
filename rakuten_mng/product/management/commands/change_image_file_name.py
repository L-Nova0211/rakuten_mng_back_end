import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from rakuten_mng.product.models import Product


class Command(BaseCommand):
    help = """
        In backend server, the image file name is like this: "10f2d336-7418-11ee-88a9-2cf05de3abd2.png"
        But Rakuten doesn't allow this format.
        The acceptable format are:
            1. Under 20 letters
            2. File format is only .jpg
    """

    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            for photo in product.productphoto_set.all():
                initial_path = f'{settings.MEDIA_ROOT}/{str(photo.path)}'
                random_name = get_random_string(15).lower()
                new_path = f'{settings.MEDIA_ROOT}/productphoto/{random_name}.jpg'
                
                os.rename(initial_path, new_path)
                photo.path = f'productphoto/{random_name}.jpg'
                photo.save()
