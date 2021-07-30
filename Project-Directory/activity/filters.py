import django_filters
from scanner.models import Visit

class VisitsFilter(django_filters.FilterSet):

    class Meta:
        model = Visit
        fields = ('barcode', 'name', 'email', 'date', 'membership', 'status' )
        
