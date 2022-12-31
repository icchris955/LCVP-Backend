from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.urls import reverse
from .models import CustomUser
from .utils.email_util import EmailUtil
from .serializers import UserSerializer


class UserRegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Email confirmation
        user = CustomUser.objects.get(email=serializer.data["email"])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        absolute_url = "http://" + current_site + relative_link + "?token=" + str(token)

        email_body = (
            "Hello "
            + user.name
            + ",\nUse this link to verify your email. \n"
            + "Verification Link: "
            + absolute_url
        )
        data = {
            "body": email_body,
            "subject": "Email Verification",
            "to": [user.email],
        }

        EmailUtil.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get("token")

        payload = AccessToken(token)
        user = CustomUser.objects.get(id=payload["user_id"])
        if not user.is_email_verified:
            user.is_email_verified = True
            user.save()
        return Response({"Email": "Successfully verified"}, status=status.HTTP_200_OK)


class AuthenticatedUserView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        name = request.user.name
        email = request.user.email
        phone = request.user.phone

        return Response(
            {
                "name": name,
                "email": email,
                "phone": phone,
                "date_joined": request.user.date_joined,
            }
        )


class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        user = get_object_or_404(CustomUser.objects.all(), pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        return Response({"success": "User '{}' updated successfully".format(user)})


    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
