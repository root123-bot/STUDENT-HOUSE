from django.shortcuts import render
from rest_framework.views import APIView
from selcom_apigw_client import apigwClient
from rest_framework import status
from rest_framework.response import Response

apiKey = 'IPATESCH-BAE4439D874TR456'
apiSecret = '1PE4412G-7J3F4K7F-2A874AF-0P636D54'
baseUrl = 'https://apigw.selcommobile.com'

client = apigwClient.Client(baseUrl, apiKey, apiSecret)


# Create your views here.
class PaymentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            orderDict = {
                "vendor":"TILL61029492",
                "order_id":"1218d5Qb",
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": "255623317196",
                "amount":  8000,
                "currency":"TZS",
                "buyer_remarks":"None",
                "merchant_remarks":"None",
                "no_of_items":  1
            }

            orderPath = "/v1/checkout/create-order-minimal"

            response = client.postFunc(orderPath, orderDict)

            print(response)

            return Response({"message": response}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
payment = PaymentAPIView.as_view()