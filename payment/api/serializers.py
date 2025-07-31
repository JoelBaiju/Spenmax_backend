from rest_framework import serializers
from shop.models import PackageOption

class PackageIdSerializer(serializers.Serializer):
    po_id = serializers.IntegerField()

    def validate(self, value):
        try:
            package_o = PackageOption.objects.get(pk=value.get("po_id"))
            if not package_o.is_active:
                raise serializers.ValidationError("invalid action")
            value["package_oiption"] = package_o
        except PackageOption.DoesNotExist:
            raise serializers.ValidationError("invalid action")

        value["amount"] = package_o.discount_price
        return value

    # def to_representation(self, instance):
    #     return {
    #         'amount': instance.price,
    #         # Add other fields you want to include from the Package model
    #     }