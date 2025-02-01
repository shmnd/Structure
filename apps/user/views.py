from rest_framework import generics,status
from base_core.helpers.response import ResponseInfo
from apps.user.serializers import UserRegistrationSerializer,UserLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from apps.user.models import User,GeneratedAccessToken
from base_core.helpers.helpers import get_object_or_none
import sys,os
from rest_framework.permissions import AllowAny
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class CreateOrUpdateUserApiView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserApiView,self).__init__(**kwargs)


    serializer_class = UserRegistrationSerializer
    @swagger_auto_schema(tags = ['Autherization'])
    def post(self,request):
        try:
            serializers = self.serializer_class(data = request.data, context={request:request})

            if not serializers.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['status'] = False
                self.response_format['errors'] = serializers.errors
                return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)
            
            user_instance = get_object_or_none(User,pk=serializers.validated_data.get('user',None))

            serializers = self.serializer_class(user_instance,data=request.data,context={'request':request})

            if not serializers.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['status'] = False
                self.response_format['errors'] = serializers.errors
                return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)    

            serializers.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format['status'] = True
            self.response_format['message'] = 'User created or updated successfully'      
            return Response(self.response_format,status=status.HTTP_201_CREATED)

        except Exception as e:
            exec_type ,exc_obj,exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f"Error occured in {exec_type},File:{fname}, line number {exc_tb.tb_lineno},Error:{str(e)}"
            return Response(self.response_format,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginApiView,self).__init__(**kwargs)

    serializer_class = UserLoginSerializer

    @swagger_auto_schema(tags=['Autherization'])
    def post(self,request):
        try:
            serializers = self.serializer_class(data=request.data)

            if not serializers.is_valid():
                    self.response_format['status'] = False
                    self.response_format['errors'] = serializers.errors
                    return Response(self.response_format,status=status.HTTP_400_BAD_REQUEST)
                
            user = auth.authenticate(
                username=serializers.validated_data.get('username',''),
                password= serializers.validated_data.get('password','')
            )
            if user:
                if not user.is_active:
                    self.response_format['status'] = False
                    self.response_format['status_code'] = status.HTTP_403_FORBIDDEN
                    self.response_format['message'] = "User is not active"
                    return Response(self.response_format,status=status.HTTP_403_FORBIDDEN)
                else:
                    serializers = UserLoginSerializer(user,context={'request':request})
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)

                    data = {
                        "user":serializers.data,
                        "token":token,
                        "refresh":str(refresh)
                    }
                    GeneratedAccessToken.objects.create(user=user,token=token)

                    self.response_format['status'] = True
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format['message'] = 'User logged in successfully' 
                    self.response_format['data'] = data
                    return Response(self.response_format,status=status.HTTP_200_OK)
            else:
                self.response_format['status'] = False
                self.response_format['status_code'] = status.HTTP_401_UNAUTHORIZED
                self.response_format['message'] = 'Invalid credentials'
                return Response(self.response_format,status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            exec_type,exc_obj,exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status'] = False  
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = f"Error occured in {exec_type},File:{fname}, line number {exc_tb.tb_lineno},Error:{str(e)}"
            return Response(self.response_format,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            




