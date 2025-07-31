from django.contrib import admin
from .models import  Category, Company, Branch , StoreImage, Package,Customer ,Offer ,Advertisement , Notification , PackageOption ,CustomerPackages,Notification_Vendor , Analytics

# Register your models here.

admin.site.register(Category)
admin.site.register(Package)

admin.site.register(Company)
admin.site.register(Branch)
admin.site.register(StoreImage)
admin.site.register(Offer)


admin.site.register(Customer)

admin.site.register(Advertisement)

admin.site.register(Notification)

admin.site.register(PackageOption)

admin.site.register(CustomerPackages)
admin.site.register(Notification_Vendor)

admin.site.register(Analytics)






