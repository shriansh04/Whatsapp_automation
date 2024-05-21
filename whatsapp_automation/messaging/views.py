# messaging/views.py
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from heyoo import WhatsApp
from django.conf import settings

from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        to = request.data.get('to')
        body = request.data.get('body')

        if not to or not body:
            print("false")
            return Response({'error': 'To and Body are required'}, status=status.HTTP_400_BAD_REQUEST)
        # whatsapp = WhatsApp(settings.HEYOO_ACCESS_TOKEN, settings.HEYOO_API_URL)
        whatsapp = WhatsApp(settings.HEYOO_ACCESS_TOKEN, phone_number_id = settings.HEYOO_PHONE_ID)
        response = whatsapp.send_message(body, to)
        

        if 'error' in response:
            return Response({'error': 'Failed to send message', 'details': response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        msg = Message.objects.create(to=to, body=body)
        serializer = self.get_serializer(msg)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def send_template(self, request):
        to = request.data.get('to')
        body = request.data.get('body')

        if not to or not body:
            print("false")
            return Response({'error': 'To and Body are required'}, status=status.HTTP_400_BAD_REQUEST)
        # whatsapp = WhatsApp(settings.HEYOO_ACCESS_TOKEN, settings.HEYOO_API_URL)
        whatsapp = WhatsApp(settings.HEYOO_ACCESS_TOKEN, phone_number_id = settings.HEYOO_PHONE_ID)
        response = whatsapp.send_template(body, to,components=[])
        

        if 'error' in response:
            return Response({'error': 'Failed to send message', 'details': response['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        msg = Message.objects.create(to=to, body=body)
        serializer = self.get_serializer(msg)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
