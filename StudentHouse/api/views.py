from django.shortcuts import render
from rest_framework.views import APIView
from selcom_apigw_client import apigwClient
from rest_framework import status
from rest_framework.response import Response
from .models import *
import base64
from django.contrib.auth import get_user_model
from rest_framework import status
import base64, requests, hmac, datetime, hashlib, json
from django.http import HttpResponse
from rest_framework.decorators import api_view

apiKey = 'IPATESCH-BAE4439D874TR456'
apiSecret = '1PE4412G-7J3F4K7F-2A874AF-0P636D54'
baseUrl = 'https://apigw.selcommobile.com'

client = apigwClient.Client(baseUrl, apiKey, apiSecret)


# Create your views here.
class PaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            amount = request.data.get('amount')

            orderDict = {
                "vendor":"TILL61029492",
                "order_id": orderId,
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "amount":  int(amount),
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

class PushUSSDPayment(APIView):
    def post(self, request):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            transId = request.data.get('transId')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'
            orderDict = {
                "vendor":"TILL61029492",
                "order_id": orderId, 
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "amount":  int(amount),
                "currency":"TZS",
                "buyer_remarks":"None",
                "merchant_remarks":"None",
                "no_of_items":  1,
                "webhook":  base64.b64encode(callback_url.encode("utf-8")).decode("utf-8")
            }

            orderPath = "/v1/checkout/create-order-minimal"
            response = client.postFunc(orderPath, orderDict)

            pushDict = {
                "transid": transId,
                "order_id": orderId,
                "msisdn": phone,
            }

            pushPath = "/v1/checkout/wallet-payment"

            response = client.postFunc(pushPath, pushDict)

            transaction = TransactionRecord.objects.create(
                transactionId = transId,
                orderId = orderId,
                payed_by = get_user_model().objects.get(id=int(user_id)),
                amount = amount
            )

            transaction.save()

            return Response({"message": response}, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)
       
push_ussd_payment = PushUSSDPayment.as_view()

# IF USER CANCELLED THE PUSH USSD IN HIS PHONE NO RESPONSE SENT TO US ON THE CALLBACK
@api_view(['POST', 'GET'])
def paymentCallBack(request):
    if request.method == 'POST':
        
        data = request.data
        transId = request.data.get('transid', None)
        orderId = request.data.get('order_id', None)
        payment_status = request.data.get('payment_status', None) # Status of the payment COMPLETED, CANCELLED, PENDING, USERCANCELED
        resultcode = request.data.get('resultcode', None)
        reference = request.data.get('reference', None) # Selcom Gateway transaction reference
        result = request.data.get('result', None) # either SUCCESS or FAIL
        print("THIS IS WHAT WE RESOLVE ", transId, orderId, payment_status, resultcode, reference)
        try:
            if (resultcode == "000"):
                transaction = TransactionRecord.objects.filter(
                    orderId = orderId,
                )
                print('THIS IS TRANSACTION FOR YOU ', transaction)
                if (transaction.count() == 0):
                    # unknown transaction 
                    print('WE DONT HAVE ANY TRANSACTION OF THAT TRANSACTION ID')
                    return Response({"message": "Unknown transaction"}, status=status.HTTP_400_BAD_REQUEST)

                transaction = transaction.last()
                transaction.status = payment_status
                transaction.save()
                if (payment_status == 'COMPLETED'):
                    print("ITS COMPLETED ")
                    # then we need here to create the Payment Records
                    payment = PaymentRecord.objects.create(
                        transaction = transaction,
                        reference = reference,
                        start_date = datetime.datetime.now(),
                        end_date = datetime.datetime.now() + datetime.timedelta(days=1),
                    )

                    payment.save()
                    return Response({"message": "Payment executed successfully"}, status=status.HTTP_200_OK)

                if (payment_status == 'USERCANCELED'):
                    print('USER CANCELLED')
                    return Response({"message": "User cancelled payment"}, status=status.HTTP_400_BAD_REQUEST)

                if (payment_status == 'CANCELED'):
                    print("ITS CANCELLED")
                    return Response({"message": "Transaction has been cancelled"}, status=status.HTTP_400_BAD_REQUEST)
               
            else:
                print('WE HAVE UNSUCCESSFUL RESULT CODE')
                return Response({"message": "Transaction failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            print('SOMETHING WENT WRONG ', str(err))
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

            # print('THIS IS DATA WE HAVE FOR YOUR CALLBACK ', data)
            # return Response({"message": "Im the post method being called"}, status=status.HTTP_200_OK)
    
payment_callback = paymentCallBack


'''
    HATIMAYE NIMEFANIKIWA KUPATA CALLBACK, NI JAMBO LA KUMSHUKURU MUNGU KILICHOBACK NI KU-CODE LOGICS
    KITU NILICHOJIFUNZA NI KWAMBA HAIFAI KUTUMIA CLASS BASED VIEW KWENYE CALLBACK  INABIDI TUTUMIE FUNCTIONAL
    BASED VIEW.. HUU MCHEZO NIMEUGUNDUA SASA HIVI BAADA YA KU-REFER CALLBACK KIPINDI NAFANYA KAZI MAINSTREAM 
    CALLBACK YAO ILIKUWA NI YA FUNCTION BASED API VIEW.. THANKY YOU GOD NA HIZI NDO SAMPLE CODE ZINAZOLETA MAJIBU
    SAHIHI


        @api_view(['POST', 'GET'])
        def paymentCallBack(request):
            print('IM FUNCTION BASED CALLBACK IM GET CALLED')
            print("THIS IS REQUEST FOR YOU ", request)
            
            if request.method == 'POST':
                data = request.data
                print('THIS IS DATA WE HAVE FOR YOUR CALLBACK ', data)
                return Response({"message": "Im the post method being called"}, status=status.HTTP_200_OK)
            
            elif request.method == 'GET':
                data = request.data
                print('THIS IS DATA WE HAVE IF ITS GET METHOD ', data)
                return Response({"message": "Im the get method being called"}, status=status.HTTP_200_OK)

        payment_callback = paymentCallBack

    NA HII NDO OUTPUT NILIYOPATA YA 'request.data'
        THIS IS DATA WE HAVE FOR YOUR CALLBACK  {'result': 'SUCCESS', 'resultcode': '000', 'order_id': 'fdUuklad', 'transid': '2019383393', 'reference': '9403111665', 'channel': 'HALOPESATZ', 'amount': '1000', 'phone': '255623317196', 'payment_status': 'COMPLETED'}
        [17/Nov/2023 22:21:33] "POST /api/malipocallback/ HTTP/1.1" 200 45



    Used PurePushUSSDPayment

    class PurePushUSSDPayment(APIView):
    def post(self, request):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            transId = request.data.get('transId')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'

            orderDict = {
                "vendor": "TILL61029492",
                "order_id": orderId,
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "amount":  int(amount),
                "currency":"TZS",
                "no_of_items":  1,
                "webhook":  base64.b64encode(callback_url.encode("utf-8")).decode("utf-8")
            }

            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            apiKey_bytes = apiKey.encode('ascii')
            base64_bytes = base64.b64encode(apiKey_bytes)
            base64_apiKey= base64_bytes.decode('ascii')

            data= "timestamp=" + timestamp
            signedFields = ""
            for key in orderDict:
                data = data + "&" + key + "=" + str(orderDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
            
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')

            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }


            orderPath = "/v1/checkout/create-order-minimal"

            url = baseUrl+orderPath
            response = requests.post(url, json=orderDict, headers=headers)
            # print('response ', response.json())

            # If it worked lets not create the push ussd request
            pushDict = {
                "transid": transId,
                "order_id": orderId,
                "msisdn": phone,
            }
            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            data= "timestamp=" + timestamp
            signedFields = ""
            for key in pushDict:
                data = data + "&" + key + "=" + str(pushDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
                        
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            print('SIGNATURE ', signature)
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')
            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }

            pushPath = "/v1/checkout/wallet-payment"

            url = baseUrl + pushPath

            

            response = requests.post(url, json=pushDict, headers=headers)
            print('response ', response.json())

            return Response({ "message": response.json()}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
pure_push = PurePushUSSDPayment.as_view()
'''


'''
class PaymentCallBack(APIView):
    def post(self, request, *args, **kwargs):
        print('IM CALLBACK BEING CALLED')
       
        transId = request.data.get('transid', None)
        orderId = request.data.get('order_id', None)
        payment_status = request.data.get('payment_status', None) # Status of the payment COMPLETED, CANCELLED, PENDING, USERCANCELED
        resultcode = request.data.get('resultcode', None)
        reference = request.data.get('reference', None) # Selcom Gateway transaction reference
        result = request.data.get('result', None) # either SUCCESS or FAIL
        print({
            "transId": transId,
            "orderId": orderId,
            "payment_status": payment_status,
            "result_code": result_code,
            "reference": reference,
            "result": result
        })
        try: 
            if (resultcode == "000"):
                transaction = TransactionRecord.objects.filter(
                    transactionId = transId,
                    orderId = orderId
                )

                if (transaction.count() == 0):
                    # unknown transaction 
                    return Response({"message": "Unknown transaction"}, status=status.HTTP_400_BAD_REQUEST)

                transaction = transaction.last()
                transaction.status = payment_status
                transaction.save()
                if (payment_status == 'COMPLETED'):
                    # then we need here to create the Payment Records
                    payment = PaymentRecord.objects.create(
                        transaction = transaction,
                        reference = reference,
                        start_date = datetime.now(),
                        end_date = datetime.now() + timedelta(days=1),
                    )

                    payment.save()
                    return Response({"message": "Payment executed successfully"}, status=status.HTTP_200_OK)

                if (payment_status == 'USERCANCELED'):
                    return Response({"message": "User cancelled payment"}, status=status.HTTP_400_BAD_REQUEST)

                if (payment_status == 'CANCELED'):
                    return Response({"message": "Transaction has been cancelled"}, status=status.HTTP_400_BAD_REQUEST)
               

            else:
                return Response({"message": "Transaction failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)

# payment_callback = PaymentAPIView.as_view()
'''

# START TO CODE WITHOUT DEPENDING ON THE apigwClient
class PurePushUSSDPayment(APIView):
    def post(self, request):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            transId = request.data.get('transId')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'

            orderDict = {
                "vendor": "TILL61029492",
                "order_id": orderId,
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "amount":  int(amount),
                "currency":"TZS",
                "no_of_items":  1,
                "webhook":  base64.b64encode(callback_url.encode("utf-8")).decode("utf-8")
            }

            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            apiKey_bytes = apiKey.encode('ascii')
            base64_bytes = base64.b64encode(apiKey_bytes)
            base64_apiKey= base64_bytes.decode('ascii')

            data= "timestamp=" + timestamp
            signedFields = ""
            for key in orderDict:
                data = data + "&" + key + "=" + str(orderDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
            
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')

            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }


            orderPath = "/v1/checkout/create-order-minimal"

            url = baseUrl+orderPath
            response = requests.post(url, json=orderDict, headers=headers)
            # print('response ', response.json())

            # If it worked lets not create the push ussd request
            pushDict = {
                "transid": transId,
                "order_id": orderId,
                "msisdn": phone,
            }
            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            data= "timestamp=" + timestamp
            signedFields = ""
            for key in pushDict:
                data = data + "&" + key + "=" + str(pushDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
                        
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            print('SIGNATURE ', signature)
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')
            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }

            pushPath = "/v1/checkout/wallet-payment"

            url = baseUrl + pushPath

            # ONLY ADDED CODE
            transaction = TransactionRecord.objects.create(
                transactionId = transId,
                orderId = orderId,
                payed_by = get_user_model().objects.get(id=int(user_id)),
                amount = amount
            )

            transaction.save()
            # WE ARE TRYING TO CREATE THE TRANSACTION HERE 

            response = requests.post(url, json=pushDict, headers=headers)
            print('response ', response.json())

            return Response({ "message": response.json()}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
pure_push = PurePushUSSDPayment.as_view()


# WORKED WITH BOTH CREATING ORDER REQUEST AND PUSH USSD
'''
    class PurePushUSSDPayment(APIView):
    def post(self, request):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            transId = request.data.get('transId')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'

            orderDict = {
                "vendor": "TILL61029492",
                "order_id": orderId,
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "amount":  int(amount),
                "currency":"TZS",
                "no_of_items":  1,
                "webhook":  base64.b64encode(callback_url.encode("utf-8")).decode("utf-8")
            }

            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            apiKey_bytes = apiKey.encode('ascii')
            base64_bytes = base64.b64encode(apiKey_bytes)
            base64_apiKey= base64_bytes.decode('ascii')

            data= "timestamp=" + timestamp
            signedFields = ""
            for key in orderDict:
                data = data + "&" + key + "=" + str(orderDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
            
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')

            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }


            orderPath = "/v1/checkout/create-order-minimal"

            url = baseUrl+orderPath
            response = requests.post(url, json=orderDict, headers=headers)
            print('response ', response.json())

            # If it worked lets not create the push ussd request
            pushDict = {
                "transid": transId,
                "order_id": orderId,
                "msisdn": phone,
            }
            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            data= "timestamp=" + timestamp
            signedFields = ""
            for key in pushDict:
                data = data + "&" + key + "=" + str(pushDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
                        
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            print('SIGNATURE ', signature)
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')
            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }

            pushPath = "/v1/checkout/wallet-payment"

            url = baseUrl + pushPath

            response = requests.post(url, json=pushDict, headers=headers)
            print('response ', response.json())

            return Response({ "message": response.json()}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
pure_push = PurePushUSSDPayment.as_view()
'''

# WORKED CREATING ORDER REQUEST
'''
class PurePushUSSDPayment(APIView):
    def post(self, request):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            transId = request.data.get('transId')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'

            orderDict = {
                "vendor": "TILL61029492",
                "order_id": orderId,
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "amount":  int(amount),
                "currency":"TZS",
                "no_of_items":  1,
                "webhook":  base64.b64encode(callback_url.encode("utf-8")).decode("utf-8")
            }

            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
           
            apiKey_bytes = apiKey.encode('ascii')
            base64_bytes = base64.b64encode(apiKey_bytes)
            base64_apiKey= base64_bytes.decode('ascii')

            data= "timestamp=" + timestamp
            signedFields = ""
            for key in orderDict:
                data = data + "&" + key + "=" + str(orderDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
            
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')

            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }


            orderPath = "/v1/checkout/create-order-minimal"

            url = baseUrl+orderPath
            response = requests.post(url, json=orderDict, headers=headers)
            print('response ', response.json)
            return Response({ "message": response.json()}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
pure_push = PurePushUSSDPayment.as_view()
'''

'''
class SampleCodePayment(APIView):
    def post(self, request):
        try:
            orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            transId = request.data.get('transId')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            
            api_secret = "1PE4412G-7J3F4K7F-2A874AF-0P636D54"
            api_key = "IPATESCH-BAE4439D874TR456"

            url = "https://apigw.selcommobile.com/v1/checkout/create-order"
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'

            data = {
                "vendor": "TILL61029492",
                "order_id": orderId,
                "buyer_email": "paschalnzwanga2015@gmail.com",
                "buyer_name": "Thabit Sadi",
                "buyer_phone": phone,
                "gateway_buyer_uuid": "",
                "amount": amount,
                "currency": "TZS",
                "payment_methods": "ALL",
                "redirect_url": base64.b64encode(callback_url.encode("utf-8")).decode("utf-8"),
                "cancel_url": base64.b64encode(callback_url.encode("utf-8")).decode("utf-8"),
                "webhook": base64.b64encode(callback_url.encode("utf-8")).decode("utf-8"),
                "billing.firstname": "Test",
                "billing.lastname": "Test",
                "billing.address_1": "969 Market",
                "billing.address_2": "",
                "billing.city": "Dar es salaam",
                "billing.state_or_region": "DA",
                "billing.country": "TZ",
                "billing.phone": phone,
                "billing.postcode_or_pobox": phone,
                "buyer_remarks": "Test Payment",
                "merchant_remarks": "Test Payment",
                "no_of_items": 1
            }
            payload = json.dumps(data)

            #timestamp = '{:%Y-%m-%dT%H:%M:%S+03:00}'.format(datetime.datetime.now())
            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
           
            signed_data="timestamp="+timestamp
            authorization = "SELCOM " + base64.b64encode(api_key.encode()).decode()

            for key, value in data.items():
                signed_data += "&"+key+"="+str(value)

            digest = hmac.new(api_secret.encode(), msg=signed_data.encode(), digestmod=hashlib.sha256,).digest()

            digest = base64.b64encode(digest).decode()

            headers = {
            'Authorization': authorization,
            'Digest-Method': 'HS256',
            'Signed-Fields': 'vendor,order_id,buyer_email,buyer_name,buyer_phone,gateway_buyer_uuid,amount,currency,payment_methods,redirect_url,cancel_url,webhook,billing.firstname,billing.lastname,billing.address_1,billing.address_2,billing.city,billing.state_or_region,billing.country,billing.phone,billing.postcode_or_pobox,buyer_remarks,merchant_remarks,no_of_items',
            'Digest': digest,
            'Timestamp': timestamp,
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            # the second logic here lets check if it will push ussd

            pushDict = {
                "transid": transId,
                "order_id": orderId,
                "msisdn": phone,
            }
            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
            data= "timestamp=" + timestamp
            signedFields = ""
            for key in pushDict:
                data = data + "&" + key + "=" + str(pushDict[key])

                # if its first time
                if (signedFields == ''):
                    signedFields = signedFields + key
                else:
                    # if its not first time
                    signedFields = signedFields + "," + key
                        
            signature = hmac.new(
                key=bytes(str(apiSecret), 'utf-8'),
                msg=bytes(data, 'utf-8'),
                digestmod=hashlib.sha256).digest()
            digestBytes = base64.b64encode(signature)
            digest = digestBytes.decode('utf-8')
            headers = {
                'Authorization': 'SELCOM ' + base64_apiKey,
                'Digest-Method': 'HS256',
                'Timestamp': timestamp,
                'Signed-Fields': signedFields,
                'Digest': digest
            }

            pushPath = "/v1/checkout/wallet-payment"

            url = baseUrl + pushPath

            response = requests.post(url, json=pushDict, headers=headers)

            return Response({ "message": response.text}, status=status.HTTP_200_OK)
        
        except Exception as err:
            print("This is error for you ", str(err))
            return Response({"message": str(err)}, status.HTTP_400_BAD_REQUEST)

sample_code = SampleCodePayment.as_view()
'''

'''
    # WORKED SAMPLE CODE 



class SampleCodePayment(APIView):
    def get(self, request):
        try:
            api_secret = "1PE4412G-7J3F4K7F-2A874AF-0P636D54"
            api_key = "IPATESCH-BAE4439D874TR456"

            url = "https://apigw.selcommobile.com/v1/checkout/create-order"
            callback_url = 'http://138.197.114.27:8000/api/malipocallback/'


            data = {
            "vendor": "TILL61029492",
            "order_id": "6056929000dfdfsd2879",
            "buyer_email": "paschalnzwanga2015@gmail.com",
            "buyer_name": "Thabit Sadi",
            "buyer_phone": "255625507057",
            "gateway_buyer_uuid": "",
            "amount": 1000,
            "currency": "TZS",
            "payment_methods": "ALL",
            "redirect_url": base64.b64encode(callback_url.encode("utf-8")).decode("utf-8"),
            "cancel_url": base64.b64encode(callback_url.encode("utf-8")).decode("utf-8"),
            "webhook": base64.b64encode(callback_url.encode("utf-8")).decode("utf-8"),
            "billing.firstname": "Test",
            "billing.lastname": "Test",
            "billing.address_1": "969 Market",
            "billing.address_2": "",
            "billing.city": "Dar es salaam",
            "billing.state_or_region": "DA",
            "billing.country": "TZ",
            "billing.phone": "255625507057",
            "billing.postcode_or_pobox": "255625507057",
            "buyer_remarks": "Test Payment",
            "merchant_remarks": "Test Payment",
            "no_of_items": 1
            }
            payload = json.dumps(data)

            #timestamp = '{:%Y-%m-%dT%H:%M:%S+03:00}'.format(datetime.datetime.now())
            now = datetime.datetime.now().astimezone()
            timestamp = now.strftime("%Y-%m-%dT%H:%M:%S%z")
           
            signed_data="timestamp="+timestamp
            authorization = "SELCOM " + base64.b64encode(api_key.encode()).decode()

            for key, value in data.items():
                signed_data += "&"+key+"="+str(value)

            digest = hmac.new(api_secret.encode(), msg=signed_data.encode(), digestmod=hashlib.sha256,).digest()

            digest = base64.b64encode(digest).decode()

            headers = {
            'Authorization': authorization,
            'Digest-Method': 'HS256',
            'Signed-Fields': 'vendor,order_id,buyer_email,buyer_name,buyer_phone,gateway_buyer_uuid,amount,currency,payment_methods,redirect_url,cancel_url,webhook,billing.firstname,billing.lastname,billing.address_1,billing.address_2,billing.city,billing.state_or_region,billing.country,billing.phone,billing.postcode_or_pobox,buyer_remarks,merchant_remarks,no_of_items',
            'Digest': digest,
            'Timestamp': timestamp,
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            return Response({ "message": response.text}, status=status.HTTP_200_OK)
        
        except Exception as err:
            print("This is error for you ", str(err))
            return Response({"message": str(err)}, status.HTTP_400_BAD_REQUEST)

sample_code = SampleCodePayment.as_view()

'''