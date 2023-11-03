import concurrent.futures
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions

from .serializers import ProductSerializer, ProductSettingSerializer
from rakuten_mng.product.models import Product, ProductSetting
from rakuten_mng.product.scrape.engineselector import select_engine
from utils.filterbackend import FilterBackend
from utils.profit_util import calc_profit


class ProductViewSet(ModelViewSet):
    permission_classes = (DRYPermissions, )
    queryset = Product.objects.all()
    filter_backends = [FilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title']
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        product_setting = ProductSetting.objects.get(created_by=request.user)
        shipping_fee = ProductSettingSerializer(product_setting).data[f'{request.data["shipping_method"]}_fee']
        product = Product.objects.get(pk=kwargs['pk'])
        profit = calc_profit(
            float(request.data['sell_price']),
            product.buy_price,
            product.count_set,
            shipping_fee,
            int(request.data['point'])
        )
        
        product.title = request.data['title']
        product.sell_price = request.data['sell_price']
        product.point = request.data['point']
        product.quantity = request.data['quantity']
        product.shipping_method = request.data['shipping_method']
        product.shipping_fee = shipping_fee
        product.profit = profit
        product.save()

        return Response(
            data='Success',
            status=status.HTTP_200_OK
        )

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
        productsetting = ProductSetting.objects.get(created_by=request.user)
        service_secret = productsetting.service_secret
        license_key = productsetting.license_key
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

    @action(detail=True, methods=['POST'])
    def patch_product(self, request, pk):
        product = Product.objects.get(pk=pk)
        product_setting = ProductSetting.objects.get(created_by=request.user)
        service_secret = product_setting.service_secret
        license_key = product_setting.license_key

        shipping_fee = ProductSettingSerializer(product_setting).data[f'{request.data["shipping_method"]}_fee']
        profit = calc_profit(
            float(request.data['sell_price']),
            product.buy_price,
            product.count_set,
            shipping_fee,
            int(request.data['point'])
        )
        resp = product.patch_to_rms(service_secret=service_secret, license_key=license_key, data=request.data)
        if resp != 'failed':
            product.title = request.data['title']
            product.sell_price = request.data['sell_price']
            product.point = request.data['point']
            product.shipping_method = request.data['shipping_method']
            product.shipping_fee = shipping_fee
            product.profit = profit
            if resp == 'success':
                product.quantity = request.data['quantity']
            product.save()

            return Response(
                data=resp,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data=resp,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['POST'])
    def bulk_deactive_product(self, request):
        product_setting = ProductSetting.objects.get(created_by=request.user)
        service_secret = product_setting.service_secret
        license_key = product_setting.license_key
        id_arr = request.data['idArray']
        data = {
            'success': [],
            'failed': []
        }
        for id in id_arr:
            product = Product.objects.get(pk=id)
            resp = product.deactive_to_rms(service_secret, license_key)
            if resp == 'success':
                data['success'].append(product.title)
            elif resp == 'falied':
                data['failed'].append(product.title)

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'])
    def bulk_remove_product_from_rakuten(self, request):
        product_setting = ProductSetting.objects.get(created_by=request.user)
        service_secret = product_setting.service_secret
        license_key = product_setting.license_key
        id_arr = request.data['idArray']
        data = {
            'success': [],
            'failed': []
        }
        for id in id_arr:
            product = Product.objects.get(pk=id)
            resp = product.remove_to_rms(service_secret, license_key)
            if resp == 'success':
                data['success'].append(product.title)
                product.productphoto_set.all().delete()
                product.delete()
            else:
                data['failed'].append(product.title)

        return Response(
            data=data,
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
