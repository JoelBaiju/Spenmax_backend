from django.db import models
from user.models import CustomUser
from shop.variables import *
from user.variable import *

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Package(models.Model):
    PACKAGE_TYPE = (
        ('BASIC', 'Basic'),
        ('COMBO', 'Combo'),
        ('ALL', 'All'),
    )
    name = models.CharField(max_length=100,unique=True)
    discription = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category,related_name='packages_c')
    created_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=PACKAGE_TYPE, default="BASIC")

class PackageOption(models.Model):  
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=0)
    package_detail = models.ForeignKey(Package,related_name="type_p",on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.package_detail.name
    
class Company(models.Model):
    user =  models.OneToOneField(CustomUser, on_delete=models.CASCADE ,related_name='detail_v', null=True, blank=True)
    organization = models.CharField(max_length=100, unique=True)
    owner = models.CharField(max_length=100)
    email_id = models.EmailField(blank=True, null=True, unique=True)
    website = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    head_office_address = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    is_registered = models.BooleanField(default=False)
    vendor_id = models.CharField(max_length=10 , unique = True)
    join_date = models.DateField(null = True , blank=True)
    notification_count = models.IntegerField(default=0)
    branch_count = models.IntegerField(default=0)

    def __str__(self):
        return self.organization if self.organization else 'Company'

class Branch(models.Model):
    SALE_TYPE_CHOICES = (
        (WHOLESALE, 'Wholesale'),
        (RETAIL, 'Retail'),
        (BOTH, 'Both'),
    )

    KeyPersonName = models.CharField(max_length=100)
    KeyPersonContact = models.CharField(max_length=20)
    PinCode = models.CharField(max_length=10)
    Locality = models.CharField(max_length=100)
    Town = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    Landphone = models.CharField(max_length=20 , blank=True ,null=True)
    RegisteredAddress = models.TextField()
    NormalWorkingHoursFrom = models.TimeField()
    NormalWorkingHoursTo = models.TimeField()
    HomeDelivery = models.BooleanField(default=False)
    google_map_link = models.URLField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    head_office = models.BooleanField(default = False)
    sales_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES, default=RETAIL)
    category = models.ForeignKey(Category, on_delete = models.PROTECT, related_name='branches_c')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.KeyPersonName}"

class StoreImage(models.Model):
    image = models.ImageField(upload_to='store_images/' , null=True , blank=True)
    branch = models.ForeignKey( Branch,on_delete=models.CASCADE , related_name='images')
    def __str__(self):
        return self.image.name

class Offer(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        (FLAT, 'Flat'),
        (PERCENTAGE, 'Percentage'),
        ("special" , 'Special')
    )

    OFFER_TYPE_CHOICES = (
        (NORMAL , "Normal"),
        (SPECIAL , "Special"),
        
    )

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default=FLAT)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='offers')
    offer_type = models.CharField(max_length=10,choices=OFFER_TYPE_CHOICES, default=NORMAL)
    offer = models.CharField(max_length=200)
    category =  models.CharField(max_length = 200 , blank=True , null=True)
    amount = models.IntegerField(default=0)
   
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email_id = models.EmailField(blank=True, null=True)
    dob = models.DateField()
    address = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    user = models.OneToOneField(CustomUser,on_delete = models.CASCADE ,related_name = "detail_c")
    number = models.CharField(max_length=13,blank=True,null=True)
    customer_id = models.CharField(max_length=10 , unique = True)
    notification_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to="profile/" , null = True , blank =True)
    join_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

class CustomerPackages(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='package_c')
    package = models.ForeignKey(PackageOption ,on_delete = models.PROTECT, related_name="packages_purchased",null=True ,default=True)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default = True)


class Advertisement(models.Model):
    PLACE_TYPE_CHOICES = [
        ("MAIN" , "Main"),
        ("NORMAL" , "Normal")
    ]

    image = models.ImageField(upload_to='advertisement_images/')
    url = models.URLField(null=True,blank=True)
    expiry_date = models.DateField()
    creation_date = models.DateField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True , related_name="advertisement")
    place = models.CharField(max_length = 50 , choices = PLACE_TYPE_CHOICES , default = "NORMAL")

    def __str__(self):
        return f"Advertisement - {self.pk}"
    
class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("UPDATE_O", 'update_o'),
        ("DELETE_O", 'delete_o'),
        ("DELETE_B", 'delete_b'),
        ("DELETE_C", 'delete_c'),
        ("REGISTER_C", 'register_c'),
        ("CONTACT" , "contact")
    ]
    
    message = models.TextField()
    offer_id = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='notification_o',blank=True,null=True)
    register_id =  models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notification_c',blank=True,null=True)
    Branch_id = models.ForeignKey(Branch , on_delete=models.CASCADE , related_name ="notification_b",blank=True,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name="notification_u",blank=True,null=True)
    approved = models.BooleanField(default=False)
    new_offer = models.CharField(max_length = 200 , null=True , blank=True)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPE_CHOICES)
    created_date = models.DateField(auto_now_add=True)
    # def __str__(self):
    #     return self.message
    
class Notification_User(models.Model):

    message = models.CharField(max_length=200)
    created_date = models.DateField(auto_now = True)

class Notification_Vendor(models.Model):

    message = models.CharField(max_length=200)
    created_date = models.DateField(auto_now = True)
    user = models.ForeignKey(Company, on_delete=models.CASCADE , related_name="notification_v_u",blank=True,null=True)


class Analytics(models.Model):

    class NameChoices(models.TextChoices):
        USER = "USER"
        PARTNER = "PARTNER"
        PACKAGE = "PACKAGE"
        USER_TARGET = "USER_TARGET"
        PARTNER_TARGET = "PARTNER_TARGET"

    name = models.CharField(max_length=50, choices=NameChoices.choices , unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - Count: {self.count}"

    








