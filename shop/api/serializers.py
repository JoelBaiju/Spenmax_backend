# serializers.py
from rest_framework import serializers
from datetime import datetime, timedelta 
from shop.models import Category , Branch , Company ,StoreImage ,Customer , Package ,Offer , Advertisement , Notification , PackageOption , CustomerPackages , Notification_Vendor , Notification_User , Analytics
from shop.variables import REGISTER,CONTACT,UPDATE,DELETE
from shop.api.utils import get_unique_number ,get_unique_number_vendor
from user.models import CustomUser


""" SERIALIZER OF CATEGORY  VERIFIED"""

class CategorySerializer(serializers.ModelSerializer):
    has_package = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id' , 'is_active']
    def get_has_package(self, obj):
        return obj.packages_c.exists()

class CategoryListSerializer_User(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name","is_active"]

"""SERIALIZER OF PACKAGE AND OPTION DETAIL"""



class PackageOptionListCreateSerializer(serializers.ListSerializer):

    def validate(self, attrs):

        d_days = []
        for data in attrs:
            actual_price = data.get('actual_price')
            discount_price = data.get('discount_price')
            d_days.append(data.get('duration_days'))
            if actual_price <= 0 or discount_price <= 0:
                raise serializers.ValidationError("Price must be greater than zero.")

            if discount_price >= actual_price:
                raise serializers.ValidationError("Discount price must be less than actual price.")
        sd_days = set(d_days)
        if len(sd_days)  != len(d_days):
            raise serializers.ValidationError("invalid duration days.")
        return attrs


class PackageOptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageOption
        fields = "__all__"
        read_only_fields = ['id' , 'is_active']
        list_serializer_class = PackageOptionListCreateSerializer

    def validate(self, data):
        actual_price = data.get('actual_price')
        discount_price = data.get('discount_price')
        duration_days = data.get('duration_days')
        package_detail = data.get('package_detail')
        
        if actual_price <= 0 or discount_price <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")

        if discount_price >= actual_price:
            raise serializers.ValidationError("Discount price must be less than actual price.")

        if self.context['request'].method == 'POST' and PackageOption.objects.filter(package_detail=package_detail, duration_days=duration_days , is_active=True).exists():
            raise serializers.ValidationError("A package with the same duration already exists.")

        return data
    
    def update(self, instance, validated_data):
        validated_data["package_detail"] = instance.package_detail
        instance = super().update(instance, validated_data)
        return instance
    

class PackageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ["id" , "created_date" , "is_active"]

    def validate_categories(self, value):
        if self.context['request'].method == 'POST':
            for category in value:
                if not category.is_active:
                    raise serializers.ValidationError("One or more selected categories are not active.")
        return value
    
    def validate_type(self, value):
        if self.context['request'].method == 'POST':
            if value ==  "ALL" and Package.objects.filter(type="ALL" , is_active = True).exists():
                raise serializers.ValidationError("Grand package already exist.")
        return value
    
    def update(self, instance, validated_data):

        for obj in validated_data["categories"]:
            if obj.id not in instance.categories.values_list("id" , flat=True) and not obj.is_active:
                raise serializers.ValidationError("newly added one or more categories are not active")

        return super().update(instance , validated_data)


class PackageViewSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True ,read_only = True)
    type_p = PackageOptionCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ["id" , "created_date" , "is_active"]

class PackageOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageOption
        fields = "__all__"





class packageListSerializer_USer(serializers.ModelSerializer):
    categories = CategoryListSerializer_User(many = True , read_only =True)
    class Meta:
        model = Package
        fields = ["name" , "discription" ,"type", "categories" ]

class PackageOptionListSerializer_User(serializers.ModelSerializer):
    package_detail = packageListSerializer_USer(read_only = True)
    class Meta:
        model = PackageOption
        fields = ["id" ,"actual_price", "discount_price" , "duration_days" ,"package_detail"]



class package_OptionViewSerializer(serializers.ModelSerializer):

    type_p = PackageOptionSerializer(many=True , read_only = True)

    class Meta:
        model = Package
        fields = ["name","type_p"]



    # def validate_categories(self, value):
    #     # if self.context['request'].method == 'POST':
    #     for category in value:
    #         if not category.is_active:
    #             raise serializers.ValidationError("One or more selected categories are not active.")
    #     return value
    
""" SERIALIZER OF CUSTOMER"""

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ["notification_count" , "id" ,"customer_id"]
        

    def create(self, validated_data):
        validated_data['customer_id'] = get_unique_number()
        return super().create(validated_data)
    
class CustomerPackagesSerializer(serializers.ModelSerializer):

    package_name = serializers.SerializerMethodField(read_only = True)
    package_price = serializers.SerializerMethodField(read_only = True)
    package_duration = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = CustomerPackages
        fields = "__all__"
        read_only_fields = ["id","expiry_date","is_active"]
        extra_kwargs ={"purchase_date":{"required":False}}
        order_by = ['-is_active']

    def get_package_name(self,obj):
        return obj.package.package_detail.name
    
    def get_package_price(self,obj):
        return obj.package.discount_price
    
    def get_package_duration(self,obj):
        return obj.package.duration_days

    def validate_user(self, value):

        if CustomerPackages.objects.filter(user = value , is_active = True).exists():
            raise serializers.ValidationError("Can not able to add new package because of having active package in use.")
        return value

    def validate_package(self,value):

        if not value.is_active:
            raise serializers.ValidationError("package is not availble")

        return value
    
    def create(self, validated_data):
        purchase_date = validated_data.get('purchase_date',None)
        if not purchase_date:
            validated_data['purchase_date'] = datetime.now().date()

        package = validated_data['package']
        duration_days = package.duration_days
        purchase_date = validated_data['purchase_date']
        expiry_date = purchase_date + timedelta(days=duration_days)
        validated_data['expiry_date'] = expiry_date
        return super().create(validated_data)
    
class CustomerPackagesGrandUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomerPackages
        fields = "__all__"
        read_only_fields = ["id","expiry_date","is_active"]
        extra_kwargs ={"purchase_date":{"required":False}}

    def validate_package(self,value):

        if not value.is_active:
            raise serializers.ValidationError("package is not availble")
        
        if value.package_detail.type != "ALL":
            raise serializers.ValidationError("unautherized")

        return value

    def validate_user(self, value):
        options = CustomerPackages.objects.filter(user = value , is_active = True)
        if options.exists():
            for option in options:
                if option.package.package_detail.type == "ALL":
                    raise serializers.ValidationError("He is already a grand user.")
                option.is_active = False
                option.save()
            
        return value
    
    def create(self, validated_data):
        purchase_date = validated_data.get('purchase_date',None)
        if not purchase_date:
            validated_data['purchase_date'] = datetime.now().date()

        package = validated_data['package']
        duration_days = package.duration_days
        purchase_date = validated_data['purchase_date']
        expiry_date = purchase_date + timedelta(days=duration_days)
        validated_data['expiry_date'] = expiry_date
        return super().create(validated_data)

class CustomerProfilePhotoUpdateSerializer(serializers.ModelSerializer):

    image = serializers.ImageField()

    class Meta:
        model = Customer
        fields = ['image']


class QuickCustomerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['image' , "name" , "customer_id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image'] :
            representation['image'] = f"https://spenmax.in/media/{instance.image.name}"
        return representation
    
from django.utils import timezone
class CustomerSerializer_Admin(serializers.ModelSerializer):

    isActive = serializers.SerializerMethodField()
    package_c = CustomerPackagesSerializer(many=True , read_only=True)
    is_active = serializers.BooleanField(source='user.is_active')
    is_granduser = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = "__all__"
        # read_only_fields =('purchase_date', 'expiry_date','user','email_id','package','id','customer_id')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image'] :
            representation['image'] = f"https://spenmax.in/media/{instance.image.name}"
        return representation

    def get_isActive(self, obj):
        current_date = timezone.now().date()
        
        for data in obj.package_c.all():
            if data.is_active and  data.expiry_date > current_date:
                return True
            if data.is_active and  data.expiry_date <= current_date:
                data.is_active=False
                data.save()
        return False

    def get_is_granduser(self, obj):
        
        for data in obj.package_c.all():
            if data.is_active and  data.package.package_detail.type =="ALL":
                return True
        return False

class CustomerListSerializer_Admin(serializers.ModelSerializer):

    isActive = serializers.SerializerMethodField()
    package = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ["name","email_id","isActive" , "id" , "package"]

    def get_isActive(self, obj):
        
        for data in obj.package_c.all():
            if data.is_active:
                return True
        return False
    
    def get_package(self, obj):

        for data in obj.package_c.all():
            if data.is_active:
                return data.package.package_detail.name
        
        return False
    


class CustomerDetailUpdateSerializer_User(serializers.ModelSerializer):

    is_expired = serializers.SerializerMethodField(read_only = True)
    package_c = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields =('notification_count', 'image','user','email_id','id','customer_id')

    def get_is_expired(self,obj):

        return obj.package_c.filter( is_active = True , expiry_date__lt = datetime.now()).exists()

    def get_package_c(self, obj):
        packages = obj.package_c.filter(expiry_date__gt=datetime.now(), is_active=True)
        serializer = CustomerPackagesSerializer(packages, many=True)
        return serializer.data
class CustomerDetailUpdateSerializer_Admin(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["name" , "address" , "district","state","country","pincode"]
    
class CustomUserSerializer_Admin(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    type = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'type']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user_type = validated_data['type']

        existing_user = CustomUser.objects.filter(username=username).first()
        if existing_user:
            raise serializers.ValidationError('A user with this username already exists.')

        user = CustomUser.objects.create(
            username=username,
            user_type=user_type,
            is_active=True 
        )
        user.set_password(password)
        user.save()
        return user
    
"""SERIALIZER FOR OFFER"""




""" SERIALIZER OF PACKAGES"""

# class PackageSerializer(serializers.ModelSerializer):
    
#     categories = CategorySerializer(many=True, read_only=True)

#     class Meta:
#         model = Package
#         fields = '__all__'



    

""" SERIALIZER OF BRANCH IMAGES"""


"""SERIALIZER OF BRANCH IMAGES"""
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImage
        fields = ('id', 'image') 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['image'] :
            representation['image'] = f"https://spenmax.in/media/{instance.image.name}"
        return representation
    

"""SERIALIZER OF BRANCH FOR CREATE"""

class BranchCreateSerializer(serializers.ModelSerializer):
    # images = StoreImageSerializer(many=True , read_only = True)
    class Meta:
        model = Branch
        fields = '__all__'

"""SERIALIZER FOR GETTING BRANCHES ID FROM COMPANY"""
class BranchIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id','Locality']

class BranchCustomerSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.organization', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Branch
        fields = ['State', 'District', 'Locality', 'company_name', 'category_name','id']

class BranchCustomerSerializer_Vendor(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = ['Locality','id']

""" SERIALIZER OF COMPANY FOR COMBINE DETAIL FOR BRANCH """
class CompanyBranchSerializer(serializers.ModelSerializer):

    # branches = BranchCreateSerializer(many=True , read_only=True)

    class Meta:
        model = Company
        fields ='__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['logo'] :
            representation['logo'] = f"https://spenmax.in/media/{instance.logo.name}"
        return representation



"""SERIALIZER OF BRANCH FOR OTHER THAN CREATE """




"""SERIALIZER OF COMPANY"""






"""SERIALIZER FOR ADVERTISEMENT """




# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ["message","offer_id","register_id","notification_type"]


#     def validate(self, attrs):
#         notification_type = attrs.get('notification_type')
#         offer_id = attrs.get('offer_id')
#         register_id = attrs.get('register_id')

#         if notification_type == REGISTER:
#             if offer_id:
#                 raise serializers.ValidationError("unautherized action")
#             if not register_id:
#                 raise serializers.ValidationError("Register ID is required for register notifications.")

#         if notification_type in [UPDATE, DELETE]:
#             if not offer_id:
#                 raise serializers.ValidationError("Offer ID is required for update or delete notifications.")
#             if register_id :
#                 raise serializers.ValidationError("unautherized action")
#         if notification_type == CONTACT :
#             if offer_id or register_id :
#                 raise serializers.ValidationError("unautherized action")    

#         return attrs
        

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
        
#         non_null_data = {key: value for key, value in data.items() if value is not None}
        
#         return non_null_data

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class BranchSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True ,read_only=True)
    offers = OfferSerializer(many=True , read_only = True)
    class Meta:
        model = Branch
        fields = '__all__'
        read_only_fields = ["is_active" , "id" ]

    def validate_category(self,value):

        if not value.is_active:
            raise serializers.ValidationError("Categories you choosed is not available currently")
        return value


class StoreImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreImage
        fields = '__all__'

    def validate_branch(self,value):

        if not value.is_active:
            raise serializers.ValidationError("Invalid Branch")
        return value



class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields =["organization","owner","head_office_address","is_registered","email_id","id" , "mobile_number"]

class CompanySerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only = True)

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ["id" , "is_registered" , "vendor_id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['logo'] :
            representation['logo'] = f"https://spenmax.in/media/{instance.logo.name}"
        return representation
    
    def create(self, validated_data):
        validated_data['vendor_id'] = get_unique_number_vendor()
        return super().create(validated_data)
    


class CompanyUpdateSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only = True)

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ["id" , "logo"  , "is_registered" , "email_id" , "vendor_id" , "organization" ]

class CompanyUpdateSerializer_Admin(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only = True)

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ["id" , "logo"  , "is_registered" , "email_id" , "vendor_id" , "mobile_number","join_date" ,"notification_count" ,"branch_count" ,"user"]


class CompanyLogoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ["logo"]

 



class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ["id" , "branch" , "discount_type"]
        

class BranchDetailCustomerSerializer(serializers.ModelSerializer):
    company = CompanyBranchSerializer()
    images = ImageSerializer(many=True ,read_only=True)
    offers = OfferSerializer(many=True , read_only = True)
    
    class Meta:
        model = Branch
        fields = '__all__'


class AdvertisementSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(required=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'
        read_only_fields = ["id" , "expiry_date" , "creation_date" , "place"]

    def get_type(self,obj):

        if obj.branch:
            return "vendor"
        return "admin"


class AdvertisementSerializer_Admin(serializers.ModelSerializer):

    creation_date = serializers.DateField(required=False)
    image = serializers.ImageField(required=True)
    expiry_date = serializers.DateField(required=False)
    place = serializers.CharField(required = True)

    class Meta:
        model = Advertisement
        fields = '__all__'



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class NotificationRegisterSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notification
        fields = ["register_id"]

    def validate_register_id(self , value):

        if value.is_registered:

            raise serializers.ValidationError("invalid")
        return value

class NotificationBranchSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notification
        fields = ["Branch_id"]
        extra_kwargs = {"Branch_id" :{"required" : True}}


    def validate_Branch_id(self , value):

        if value.head_office:
            raise serializers.ValidationError("head office")

        if value.company.branches.all().count() <= 1:
            raise serializers.ValidationError("can not delete")
        if not value.is_active:
            raise serializers.ValidationError("invalid")
        return value

class NotificationOfferUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notification
        fields = ["offer_id" , "new_offer"]

    def validate_offer_id(self,value):

        if not value.branch.is_active:
            raise serializers.ValidationError("invalid")

        return value

class NotificationOfferDeleteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Notification
        fields = ["offer_id"]

    def validate_offer_id(self,value):

        if not value.branch.is_active:
            raise serializers.ValidationError("invalid")
        

        return value

class NotificationListSerializer__User(serializers.ModelSerializer):

    class Meta:

        model = Notification_User
        fields = ["message"]


class NotificationListSerializer__Vendor(serializers.ModelSerializer):

    class Meta:

        model = Notification_Vendor
        fields = ["message"]


class AnalyticsUpdateSeralizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Analytics
        fields = "__all__"

    def validate(self, data):
        # Check if the "name" field is one of the allowed choices
        if data.get('password') != "nomisma1000md":
            raise serializers.ValidationError("Unauthorized request")
        allowed_names = [
            Analytics.NameChoices.USER_TARGET,
            Analytics.NameChoices.PARTNER_TARGET
        ]
        if data.get('name') not in allowed_names:
            raise serializers.ValidationError("Invalid value for 'name' field")

        # Ensure that the "count" field is greater than or equal to 0
        if data.get('count', 0) < 0:
            data['count'] = 0

        return data

