from django.shortcuts import render
from rest_framework.views import APIView
from selcom_apigw_client import apigwClient
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
import base64
from django.contrib.auth import get_user_model
from rest_framework import status
import base64, requests, hmac, datetime, hashlib, json
from django.http import HttpResponse
from rest_framework.decorators import api_view
import random, json
from django.db.models import Q
from StudentHouse.organization.models import *

apiKey = 'IPATESCH-BAE4439D874TR456'
apiSecret = '1PE4412G-7J3F4K7F-2A874AF-0P636D54'
baseUrl = 'https://apigw.selcommobile.com'

client = apigwClient.Client(baseUrl, apiKey, apiSecret)

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
                    print("ITS COMPLETED THIS IS PAYENT STATUS ", payment_status)
                    # then we need here to create the Payment Records
                    # lets get the transaction metadata to save on payment if completed
                    metadata = transaction.metadata
                    metadata = json.loads(metadata)
                    if metadata['type'].lower() == 'Institute'.lower():
                        # we're in institute
                        start_date = metadata['date']
                        start_date = start_date.split(' ')[0]
                        duration = metadata['duration']
                        payment = PaymentRecord.objects.create(
                            transaction = transaction,
                            reference = reference,
                            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d"),
                            end_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=int(duration)),
                        )

                        payment.save()
                        serializer = PaymentRecordSerializer(payment)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    
                    elif metadata['type'].lower() == 'mzazi'.lower():
                        # we are in parent
                        # start_date = metadata['date']
                        # start_date = start_date.split(' ')[0]
                        # duration = metadata['duration']
                        student_metadata = json.loads(metadata['student_metadata'])
                        print('THIS IS METADATA FOR YOU BOYS ', student_metadata)
                        payments = []

                        for data in student_metadata:
                            # we said we should create payment record for each data, start_date should come from "data" also the
                            # duration should come from data
                            student = Student.objects.get(id=int(data['student_id']))
                            start_date = data['start_date']
                            start_date = start_date.split(' ')[0]
                            duration = data['duration']
                            amount = data['init_amount']
                            payment = PaymentRecord.objects.create(
                                transaction = transaction,
                                reference = reference,
                                student = student,
                                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d"),
                                end_date = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=int(duration)),
                                amount = amount
                            )
                            
                            payments.append(payment)
                            payment.save()
                        
                        serializer = PaymentRecordSerializer(payments, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)


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



# START TO CODE WITHOUT DEPENDING ON THE apigwClient
class PurePushUSSDPayment(APIView):
    def post(self, request):
        try:
            # orderId = request.data.get('orderId')
            phone = request.data.get('phone')
            amount = request.data.get('amount')
            user_id = request.data.get('user_id')
            metadata = request.data.get("metadata", None)
            callback_url = 'http://138.197.114.27/api/malipocallback/'
            print('THIS IS METADATA ', metadata, phone, amount, user_id)
            # metadata = json.loads(metadata) if metadata else None
            # print('THIS. ISMETADATA FOR YOU ', metadata)
            # {'type': 'Institute', 'duration': '30', 'date': '2023-11-24 13:30:31.029662'}
            # lets generate the transId and orderId
            existings_orders = TransactionRecord.objects.values_list('orderId', flat=True)
            # existings_trans = 
            orderId = ''
            flag = True
            while flag:
                orderId = str(random.randint(1000000000000000000, 99999999990000000000))
                if orderId not in existings_orders:
                    flag = False

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
                "transid": orderId + '=trans',
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
                orderId = orderId,
                payed_by = get_user_model().objects.get(id=int(user_id)),
                amount = amount,
                metadata = metadata,
            )

            transaction.save()
            # WE ARE TRYING TO CREATE THE TRANSACTION HERE 

            response = requests.post(url, json=pushDict, headers=headers)
            print('response ', response.json())

            return Response({ "message": response.json()}, status=status.HTTP_200_OK)

        except Exception as e:
            print('ERROR FOR YOU ', str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
pure_push = PurePushUSSDPayment.as_view()


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


class PaymentRecordsByUser(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user = get_user_model().objects.get(id=int(user_id))

        payments = PaymentRecord.objects.filter(Q(user = user) | Q(transaction__payed_by = user))

        payments = reversed(payments)

        serializer = PaymentRecordSerializer(payments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

user_payments = PaymentRecordsByUser.as_view()