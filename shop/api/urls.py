from django.urls import path
from shop.api import views
app_name = "shop"

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('packages/' ,views.PackageListView.as_view() , name='packages-list'),
    path('packages/create/', views.PackageCreateView.as_view(), name='packages-create'),
    path('packages/<int:pk>/', views.PackageDetailView.as_view(), name='packages-detail'),
    path('packages/<int:pk>/update/', views.PackageUpdateView.as_view(), name='packages-update'),
    path('packages/<int:pk>/delete/', views.PackageDeleteView.as_view(), name='packages-delete'),
    path("packages/options/" , views.Package_OptionsListView.as_view() , name="packages-option-list"),

    path("package_option/create/" , views.PackageOptionCreateView.as_view() , name="packages-option-create"),
    path("package_option/<int:pk>/update/" , views.PackageOptionUpdateView.as_view() , name="packages-option-update"),
    path("package_option/<int:pk>/delete/" , views.PackageOptionDeleteView.as_view() , name="packages-option-delete"),
    path("package_option/user/" , views.PackageOptionListView_User.as_view() , name="packages-option-list"),
    path("package_option/all_user/" , views.PackageOptionListView_AllUser.as_view() , name="packages-option-list-alluser"),

    path("customer/",views.CustomerListView_Admin.as_view(),name="customer-list"),
    path("customer/<int:pk>/" , views.CustomerDetailView_Admin.as_view() , name="customer-detail"),
    path("customer/create/", views.CustomerCreateView.as_view(), name='customer-create'),
    path("customer/<int:pk>/delete/", views.CustomerDeleteView.as_view(), name='customer-delete'),
    path("customer/package/update/" , views.CustomerPackageUpdateView.as_view() , name="customer-package-update"),
    path("customer/package/grand-update/" , views.CustomerPackageGrandUpdateView.as_view() , name="customer-package-grand-update"),
    #user side
    path("customer/detail_update/user/" , views.CustomerUpdateDetailView.as_view() , name="customer-detail-user"),
    path("customer/update/<int:pk>/admin/" , views.CustomerUpdateDetailView_Admin.as_view() , name="customer-update-admin"),
    path("customer/update_profile/user/" , views.CustomerUpdateProfilePhotoView_User.as_view() , name="customer-update-profile-user"),
    path("customer/photo/<int:pk>/update/user/" , views.CustomerUpdateProfilePhotoView_User.as_view() , name="customer-update-profile-user"),
    path("customer/quick_profile/user/" , views.QuickCustomerDetailView.as_view() , name="customer-quick-profile-user"),


    path('vendor/company/', views.CompanyListView.as_view(), name='company-list'),
    path('vendor/company/create/', views.CompanyCreateView.as_view(), name='company-create'),
    path('vendor/company/<int:pk>/',views.CompanyDetailView.as_view(), name='company-detail'),
    path('vendor/company/<int:pk>/update/',views.CompanyUpdateView.as_view(), name='company-update'),
    path('vendor/company/<int:pk>/a_update/',views.CompanyUpdateView_Admin.as_view(), name='company-update-admin'),
    path('vendor/company/<int:pk>/a_delete/',views.DeleteCompanyView_Admin.as_view(), name='company-delete-admin'),
    path('vendor/company/<int:pk>/delete/',views.CompanyDeleteView.as_view(), name='company-delete'),
    path('vendor/company/<int:pk>/logo/edit/',views.CompanyLogoUpdateView.as_view(), name='company-logo-update'),
    # path('vendor/company/<int:pk>/register/', views.CompanyRegistrationAPIView.as_view(), name='company-register'),
    path('vendor/company/<int:pk>/verify/' ,views.CompanyVerification , name="company-verification"),
    path('vendor/company/<int:company_id>/branches/', views.CompanyBranchListView.as_view(), name='company-branches'),
    path('vendor/company/detail/',views.CompanyDetailView_Vendor.as_view(), name='company-detail-vendor'),

    path('vendor/branches/create/', views.BranchCreateView.as_view(), name='branch-create'),
    path('vendor/branches/', views.BranchListView.as_view(), name='branch-list'),
    path('vendor/branches/<int:pk>/', views.BranchDetailView.as_view(), name='branch-detail'),
    path('vendor/branches/<int:pk>/update/', views.BranchUpdateView.as_view(), name='branch-update'),
    path('vendor/branches/<int:pk>/delete/', views.BranchDeleteView.as_view(), name='branch-delete'),
    path('vendor/branches/customer/', views.BranchListViewCustomer.as_view() , name='branch-list-customer'),
    path('vendor/branches/user/', views.BranchListView_User.as_view() , name='branch-list-customer'),
    path('vendor/branches/customer/<int:pk>/', views.BranchDetailViewCustomer.as_view(), name='branch-detail-customer'),
    path("vendor/branches/image/<int:pk>/delete/" , views.ImageDeleteView.as_view() ,name="image-delete"),
    path("vendor/branches/image/create/" ,views.ImageCreateView.as_view() , name="image-create"),
    path('branches/vendor/', views.BranchListViewVendor.as_view() , name='branch-list-vendor'),

    path('branches/<int:pk>/offers/', views.OfferListAPIView.as_view(), name='offer-list'),
    path('branches/offers/create/', views.OfferCreateAPIView.as_view(), name='offer-list-create'),

    path('advertisements/', views.AdvertisementListView.as_view(), name='advertisement-list'),
    path('advertisements/customer/', views.AdvertisementListViewCustomer.as_view(), name='advertisement-list-customer'),
    path('advertisements/<int:pk>/branch/', views.AdvertisementListViewCustomer_Branch.as_view(), name='advertisement-list-customer-branch'),
    path('advertisements/vendor/', views.AdvertisementListViewVendor.as_view(), name='advertisement-list-vendor'),
    path('advertisements/create/admin/', views.AdvertisementCreateView_Admin.as_view(), name='advertisement-create'),
    path('advertisements/create/', views.AdvertisementCreateView.as_view(), name='advertisement-create'),
    path('advertisements/<int:pk>/', views.AdvertisementDetailView.as_view(), name='advertisement-detail'),

    path('notification/register/' , views.NotificationRegisterAPIView.as_view() , name="notification-register"),
    path('notification/vendor/branch/delete/' , views.NotificationBranchAPIView.as_view() , name="notification-branch-delete"),
    path('notification/vendor/offer/update/' , views.NotificationOfferUpdateAPIView.as_view() , name="notification-offer-update"),
    path('notification/vendor/offer/delete/' , views.NotificationOfferDeleteAPIView.as_view() , name="notification-offer-delete"),
    path('notification/<int:pk>/', views.NotificationAprovalAPIView.as_view(), name='notification-aproval'),
    path('notification/user/', views.NotificationListViewCustomer.as_view(), name='notification-list-user'),
    path('notification/vendor/', views.NotificationListViewVendor.as_view(), name='notification-list-vendor'),
    path('notification/admin/', views.NotificationListViewAdmin.as_view(), name='notification-list-admin'),
    path("notification/count/user/" , views.notification_count_user , name="notification-count-user"),
    path("notification/count/vendor/" , views.notification_count_vendor , name="notification-count-vendor"),
    path("notification/count/admin/" , views.notification_count_admin , name="notification-count-admin"),


    path("analytics/customer/" , views.CustomerAnalyticsAPIView.as_view() , name="analytics-customer"),
    path("analytics/partner/" , views.PatnerAnalyticsAPIView.as_view() , name="analytics-customer"),
    path("analytics/target/update/" , views.UpdateTargetAPIView.as_view() , name="analytics-target-update"),
    path("analytics/user/count/" , views.AnalyticsUserCountAPIView.as_view() , name="analytics-user-count"),
path('delete-all-vendors/', views.DeleteAllVendorDataView.as_view(), name='delete_all_vendors'),
]   

"""register company, delete company, delete branch , update offer , delete offer"""

""""""
