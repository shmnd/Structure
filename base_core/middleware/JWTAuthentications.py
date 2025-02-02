from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.user.models import GeneratedAccessToken


class BlackListedTokenAuthentication(JWTAuthentication):
    def authenticate(self,request):
        token = super().authenticate(request)
        print(token,'tokennnnnnnnnnnnnn')
        fil_token = GeneratedAccessToken.objects.filter(token=str(token[1])).exists()
        print(fil_token,'fil_tokennnnnnnnnnnnnn')
        if token and fil_token:
            return token
        return None