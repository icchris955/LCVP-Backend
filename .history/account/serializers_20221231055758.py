from rest_framework.serializers import ModelSerializer
from .models import (
    CustomUser,
    AdditionalInfo,
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "public_id",  # uuid
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
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AdditionalInfoSerializer(ModelSerializer):
    class Meta:
        model = AdditionalInfo
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "address",
            "province",
            "district",
            "sector",
            "about",
        )
