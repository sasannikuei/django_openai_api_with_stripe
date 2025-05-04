from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.shortcuts import render
import os
from dotenv import load_dotenv
load_dotenv()
import logging
from .serializers import PaymentSerializer
from .models import Payment
import stripe

logger = logging.getLogger(__name__)

my_api_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = my_api_key


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class CreatePaymentIntentView(APIView):
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency')
        email = request.data.get("user_email")
        if not email:
            return Response({'error': 'Invalid email'}, status=400)
        if not amount or int(amount) <= 0:
            return Response({'error': 'Invalid amount'}, status=400)
        if not currency:
            return Response({'error': 'Currency is required'}, status=400)

        try:
            # Create the Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount),  # Amount in cents
                currency=currency,
            )

            # Save to the database
            payment_data = {
                'amount': amount,
                'currency': currency,
                'stripe_payment_id': intent['id'],
                'user_email': email
            }
            serializer = PaymentSerializer(data=payment_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'clientSecret': intent['client_secret'],
                    'payment': serializer.data,

                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=400)




def test_func(request):
    html = '<html lang="en"><body>Hello you.</body></html>'
    return HttpResponse(html)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email
        })





client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

class TableGenerator(APIView):
    def post(self, request):
        logger.info("Received POST request to /api/table/")

        # if client is None:
        #     logger.error("API key is missing")
        #     return Response({'error': 'OpenAI API key is not set'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prompt = request.data.get('prompt', '')


        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            logger.info("OpenAI response received")

            table_html = response.choices[0].message.content
            return Response({'table_html': table_html}, status=status.HTTP_200_OK)



        except Exception as e:
            logger.exception("Error while calling OpenAI API")

            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
