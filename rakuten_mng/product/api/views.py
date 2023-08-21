import concurrent.futures
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions

from .serializers import ProductSerializer
from rakuten_mng.product.models import Product
from rakuten_mng.product.scrape.engineselector import select_engine


class ProductViewSet(ModelViewSet):
    permission_classes = (DRYPermissions, )
    queryset = Product.objects.all()
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
