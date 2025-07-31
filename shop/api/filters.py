import django_filters
from shop.models import Branch , Category , Customer , PackageOption



class CategoryFilter(django_filters.FilterSet):

    class Meta:
        model= Category
        fields = ["is_active"]

class BranchFilter(django_filters.FilterSet):

    class Meta:
        model = Branch
        fields = ['category__name']


class PackageOptionFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="package_detail__type")
    class Meta:
        model = PackageOption
        fields = ["type"]

class CustomerFilter(django_filters.FilterSet):
    verified = django_filters.BooleanFilter(field_name="user__is_active")
    package = django_filters.CharFilter(method="filter_package")
    is_active =django_filters.CharFilter(method="filter_is_active")

    class Meta:
        model = Customer
        fields = ['verified', 'package' , "is_active"]


    def filter_package(self, queryset, name, value):
        
        if value:
            filtered_customer_ids = []
            for customer in queryset:
                for package in customer.package_c.filter(is_active=True, package__package_detail=value):
                    filtered_customer_ids.append(customer.pk)
                    break  # Stop checking other packages for this customer
            return queryset.filter(pk__in=filtered_customer_ids)
        return queryset
    
    def filter_is_active(self, queryset, name, value):
       
        if value == "True":
            filtered_customer_ids = []
            for customer in queryset:
                for package in customer.package_c.filter(is_active=value):
                    filtered_customer_ids.append(customer.pk)
                    break
            return queryset.filter(pk__in=filtered_customer_ids)
        
        elif value == "False":
            filtered_customer_ids = []
            for customer in queryset:
                if not customer.package_c.exists() or not customer.package_c.filter(is_active=True).exists():
                    filtered_customer_ids.append(customer.pk)
            return queryset.filter(pk__in=filtered_customer_ids)
        
        return queryset
