from rest_framework.serializers import ModelSerializer
from .models import (CustomUser, AdditionalInfo,)


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "public_id", #uuid
            "nid",
            
        ]