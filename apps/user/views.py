from rest_framework import generics,status
from base_core.helpers.response import ResponseInfo
from apps.user.serializers import UserRegistrationSerializer,UserLoginSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from apps.user.models import User
from base_core.helpers.helpers import get_object_or_none
import sys,os
# Create your views here.

class CreateOrUpdateUserApiView(generics.GenericAPIView):
    
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserApiView,self).__init__(**kwargs)

    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(tags = ['Autherization'])
    def post(self,request):
        # try:
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

        # except Exception as e:
            exec_type ,exc_obj,exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f"Error occured in {exec_type},File:{fname}, line number {exc_tb.tb_lineno},Error:{str(e)}"
            return Response(self.response_format,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class LoginApiView(generics.GenericAPIView):
#     def __init__(self, **kwargs):
#         self.response_format = ResponseInfo().response
#         super(LoginApiView,self).__init__(**kwargs)

#     serializer_class = UserLoginSerializer

#     @swagger_auto_schema(tags=['Autherization'])





