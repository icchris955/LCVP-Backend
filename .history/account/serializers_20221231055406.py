from rest_framework.serializers import ModelSerializer
from .models import (CustomUser, AdditionalInfo,)


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "public_id", #uuid
            "nid",
            "name",
            "email",
            "phone",
            "password",
            "account_type",
            "is_active",
            "is_admin",
            "is_email_verified",
            "date_of_creation",
        ]


