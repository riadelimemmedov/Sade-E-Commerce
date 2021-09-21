import django_filters
from django_filters import DateFilter,CharFilter
from .models import  *#yeni modeldeki ne varsa getirirem bura


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name = 'date_created', lookup_expr= 'gte')#field_name de qeyd edirsen yeni modeldeki date_created yeri looup ise orani filterleyir gte ise greater than ozunden boyuk
    end_date = DateFilter(field_name='date_created', lookup_expr= 'lte')#!Yeniki meselen gte de 2005 den boyukler amma lte de olsa olacag 2005 den kicikler gte greater than ozunden boyuk lte less than ozunden kicik
    class Meta:
        model = Order#yeni deyremki Order classini istifade edirem modelden gelen Order classi yeni
        fields = '__all__'#__all__  vasitesile butun fieldlari secirem
        exclude = ['customer','date_created']
        