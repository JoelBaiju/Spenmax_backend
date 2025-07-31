from django.urls import include, path
from django.contrib import admin
from payment.api.views import PaymentView , CallbackView
urlpatterns = [
    path('razorpay_order/', PaymentView.as_view(), name='razorpay_order'),
    path('razorpay_callback/', CallbackView.as_view(), name='razorpay_callback'),
]