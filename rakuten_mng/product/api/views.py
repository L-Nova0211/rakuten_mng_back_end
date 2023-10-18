import concurrent.futures
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions

from .serializers import ProductSerializer, ProductSettingSerializer
from rakuten_mng.product.models import Product, ProductSetting
from rakuten_mng.product.scrape.engineselector import select_engine
from utils.filterbackend import FilterBackend


class ProductViewSet(ModelViewSet):
    permission_classes = (DRYPermissions, )
    queryset = Product.objects.all()
    filter_backends = [FilterBackend]
    filterset_fields = ['status']
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

    @action(detail=False, methods=['POST'])
    def scrape_data(self, request):
        url = request.data['url']
        engine = select_engine(url=url)
        if engine:
            engine = engine()
            try:
                data = engine.scrape_item_list(source_url=url)
                products = []
                created_by = request.user
                pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(data))
                for item in data:
                    pool.submit(Product.save_product, data=item, products=products, created_by=created_by)
                    
                pool.shutdown(wait=True)

                return Response(
                    data=self.serializer_class(products, many=True).data,
                    status=status.HTTP_200_OK
                )
            except Exception as err:
                raise err
        
        return Response(
            data='入力したサイトへのサービスはまだサポートされていません。',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['POST'])
    def insert_products(self, request):
        service_secret = request.user.service_secret
        license_key = request.user.license_key
        id_arr = request.data['idArray']
        data = {
            'success': [],
            'incomplete': [],
            'failed': []
        }
        for id in id_arr:
            product = Product.objects.get(pk=id)
            resp = product.insert_to_rms(
                service_secret=service_secret,
                license_key=license_key
            )
            if resp == 'success':
                data['success'].append(product.title)
            elif resp == 'incomplete':
                data['incomplete'].append(product.title)
            elif resp == 'falied':
                data['failed'].append(product.title)
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'])
    def bulk_remove_product(self, request):
        id_arr = request.data['idArray']
        for id in id_arr:
            product = Product.objects.get(pk=id)
            product.productphoto_set.all().delete()
            product.delete()

        return Response(
            data='操作が成功しました。',
            status=status.HTTP_200_OK
        )


class ProductSettingViewSet(ModelViewSet):
    permission_classes = (DRYPermissions, )
    queryset = ProductSetting.objects.all()
    serializer_class = ProductSettingSerializer

    def get_queryset(self):
        return ProductSetting.objects.filter(created_by=self.request.user)
    
    @action(detail=False, methods=['POST'])
    def register(self, request):
        productsetting = ProductSetting(
            license_key=request.data['apiKey'],
            service_secret=request.data['serviceSecret'],
            shipping_mail_fee=request.data['shippingMail'],
            shipping_60_fee=request.data['shipping60'],
            shipping_80_fee=request.data['shipping80'],
            shipping_100_fee=request.data['shipping100'],
            shipping_120_fee=request.data['shipping120'],
            scraping_update_amazon_from=request.data['updateAmazon'],
            scraping_update_oroshi_from=request.data['updateOroshi'],
            scraping_update_tajimaya_from=request.data['updateTajimaya'],
            rakuten_fee=request.data['rakutenFee'],
            created_by=request.user
        )
        productsetting.save()

        return Response(
            data=self.serializer_class(productsetting).data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'])
    def change(self, request):
        productsetting = ProductSetting.objects.get(created_by = request.user)
        productsetting.license_key=request.data['apiKey']
        productsetting.service_secret=request.data['serviceSecret']
        productsetting.shipping_mail_fee=request.data['shippingMail']
        productsetting.shipping_60_fee=request.data['shipping60']
        productsetting.shipping_80_fee=request.data['shipping80']
        productsetting.shipping_100_fee=request.data['shipping100']
        productsetting.shipping_120_fee=request.data['shipping120']
        productsetting.scraping_update_amazon_from=request.data['updateAmazon']
        productsetting.scraping_update_oroshi_from=request.data['updateOroshi']
        productsetting.scraping_update_tajimaya_from=request.data['updateTajimaya']
        productsetting.rakuten_fee=request.data['rakutenFee']
        productsetting.created_by=request.user
        productsetting.save()

        return Response(
            data=self.serializer_class(productsetting).data,
            status=status.HTTP_200_OK
        )
