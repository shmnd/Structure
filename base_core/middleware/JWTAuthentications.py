from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.user.models import GeneratedAccessToken


class BlackListedTokenAuthentication(JWTAuthentication):
    def authenticate(self,request):
        token = super().authenticate(request)
        if token and GeneratedAccessToken.objects.filter(token=str(token[1])).exists():
            return token
        return None