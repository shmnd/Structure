from rest_framework import generics
from base_core.helpers.response import ResponseInfo
from apps.user.serializers import UserRegistrationSerializer
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class CreateOrUpdateUserApiView(generics.GenericAPIView):
    
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserApiView,self).__init__(**kwargs)

    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(tags = ['Autherization'])

    


