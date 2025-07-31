import json
import os
import razorpay
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta


# from payments.constants import PaymentStatus
from payment. models import RazorpayPayment
from payment.api import serializers
from user.api.permissions import IsUserType , IsUserAndNoPackage
from shop.models import CustomerPackages
# Get Razorpay Key id and secret for authorizing razorpay client.
RAZOR_KEY = settings.RAZOR_KEY
RAZOR_SECRET = settings.RAZOR_SECRET

# Creating a Razorpay Client instance.
razorpay_client = razorpay.Client(auth=(RAZOR_KEY, RAZOR_SECRET))


class PaymentView(APIView):

    permission_classes = [IsUserAndNoPackage]

    @staticmethod
    def post(request, *args, **kwargs):

        serializer = serializers.PackageIdSerializer(data = request.data)

        serializer.is_valid(raise_exception = True)

        amount = serializer.validated_data["amount"]
        po_id = serializer.validated_data["package_oiption"]
        # Create Order
        razorpay_order = razorpay_client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )

        # Save the order in DB
        order = RazorpayPayment.objects.create(
            user=request.user, amount=amount, provider_order_id=razorpay_order["id"] , package_option = po_id
        )

        data = {
            "name" : request.user.detail_c.name,
            "merchantId": RAZOR_KEY,
            "amount": amount,
            "currency" : 'INR' ,
            "orderId" : razorpay_order["id"],
        }

        # # save order Details to frontend
        return Response(data, status=status.HTTP_200_OK)
        # return Response({"demo" : "up to success.."}, status=status.HTTP_200_OK)


class CallbackView(APIView):
    
    """
    APIView for Verifying Razorpay Order.
    :return: Success and failure response messages
    """
    permission_classes = [IsUserAndNoPackage]


    @staticmethod
    def post(request, *args, **kwargs):

        if not request.data:
            return Response({'status': 'Invalid action with out necessery data.'}, status=status.HTTP_400_BAD_REQUEST)

        response = request.data.get("Response" , None)

        if not response:
            response = request.data.get("error",None)
        """
            if razorpay_signature is present in the request 
            it will try to verify
            else throw error_reason
        """
        if "razorpay_signature" in response:

            # Verifying Payment Signature
            data = razorpay_client.utility.verify_payment_signature(response)

            # if we get here True signature
            if data:
                payment_object = RazorpayPayment.objects.get(provider_order_id = response['razorpay_order_id'])                # razorpay_payment = RazorpayPayment.objects.get(order_id=response['razorpay_order_id'])
                payment_object.status = RazorpayPayment.PaymentStatus.SUCCESS
                payment_object.payment_id = response['razorpay_payment_id']
                payment_object.signature_id = response['razorpay_signature']          
                payment_object.save()
                duration_days = payment_object.package_option.duration_days
                current_date = datetime.now().date()
                expiry_date = current_date + timedelta(days=duration_days)
                CustomerPackages.objects.create(user = payment_object.user.detail_c , package= payment_object.package_option , purchase_date = current_date , expiry_date = expiry_date)
                return Response({'status': 'Payment Done'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Signature Mismatch!'}, status=status.HTTP_400_BAD_REQUEST)

        # Handling failed payments
        else:
            error_code = response["code"]
            error_description = response["description"]
            error_source = response["source"]
            error_reason = response["reason"]
            # error_metadata = json.loads(response["metadata"])
            razorpay_payment =   RazorpayPayment.objects.get(provider_order_id=response["metadata"]['order_id'])
            razorpay_payment.payment_id = response["metadata"]['payment_id']
            razorpay_payment.signature_id = "None"
            razorpay_payment.status = RazorpayPayment.PaymentStatus.FAILED
            razorpay_payment.save()

            error_status = {
                'error_code': error_code,
                'error_description': error_description,
                'error_source': error_source,
                'error_reason': error_reason,
            }

            return Response({'error_data': error_status}, status=status.HTTP_401_UNAUTHORIZED)