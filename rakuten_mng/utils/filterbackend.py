from django_filters import rest_framework


class FilterBackend(rest_framework.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if(request.query_params.get('status') == 'notDraft'):
            queryset = queryset.exclude(status='Draft')
            return queryset

        return super().filter_queryset(request, queryset, view)
