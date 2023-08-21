import requests
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from dry_rest_permissions.generics import authenticated_users
from PIL import Image


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft' # Not Publish yet
        INCOMPLETE = 'Incomplete' # Publish, but has some errors
        INACTIVE = 'Inactive' # Publish, but not Active
        ACTIVE = 'Active' # Publish, Active

    class Condition(models.TextChoices):
        NEW = 'new_new'

    status = models.CharField(
        _('status'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    source_url = models.TextField(_('url'), null=True, blank=True)
    title = models.CharField(
        _('title'),
        max_length=255,
        null=True,
        blank=True
    )
    condition = models.CharField(
        _('condition'),
        max_length=20,
        blank=True,
        choices=Condition.choices
    )
    buy_price = models.IntegerField(
        _('buy Price'),
        null=True,
        blank=True
    )
    sell_price = models.IntegerField(
        _('sell Price'),
        null=True,
        blank=True
    )
    quantity = models.IntegerField(
        _('quantity'),
        null=True,
        blank=True
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        "users.user",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    @classmethod
    def save_product(cls, data, products, created_by):
        product = Product(
            status=Product.Status.DRAFT,
            source_url=data['source_url'],
            title=data['title'],
            condition=Product.Condition.NEW,
            # TODO
            # condition=data['condition'],
            buy_price=data['price'],
            sell_price=data['price']*2,
            quantity=1,
            # TODO
            # quantity=data['quantity'],
            # point=data['point'],
            description=data['description'],
            created_by=created_by
        )
        product.save()

        # Photo
        photos = data['photos']
        for (index, photo) in enumerate(photos):
            image = requests.get(photo['url'])
            random_name = uuid.uuid1()
            with open(str(settings.APPS_DIR/ f'media/productphoto/{random_name}.png'), 'wb') as f:
                f.write(image.content)
            image = Image.open(str(settings.APPS_DIR/ f'media/productphoto/{random_name}.png'))
            productphoto = ProductPhoto(
                product=product,
                path=f'productphoto/{random_name}.png',
                width=image.width,
                height=image.height
            )
            productphoto.save()
            if index >= 8:
                break # Amazon allows maximium 9 Images
        products.append(product)

    @authenticated_users
    def has_read_permission(request):
        return True
    
    @authenticated_users
    def has_write_permission(request):
        return True


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        "product.Product", null=True, blank=True, on_delete=models.SET_NULL
    )
    path = models.ImageField(
        _('image file'),
        upload_to="productphoto"
    )
    width = models.DecimalField(
        _('width'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    height = models.DecimalField(
        _('height'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
