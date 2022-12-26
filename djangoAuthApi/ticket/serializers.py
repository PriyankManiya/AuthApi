from rest_framework import serializers
from ticket.models import Tickets
# from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ('id', 'creatorid', 'resolverid',  'isresolved',
                  'resolveddate', 'is_active', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
