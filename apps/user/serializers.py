from rest_framework import serializers
from apps.user.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken,TokenError

class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)    
    password = serializers.CharField(write_only=True,required=True)
    confirm_password =serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['email','username','full_name','gender','phone_number','password','confirm_password','profile_image']

        extra_kwargs = {
            'password' : {'write_only':True},
            'confirm_password' : {'write_only':True}
        }

    def validate(self,data):
        password            = data.get('password')
        confirm_password    = data.get('confirm_password')
        username           = data.get('username')
        email               = data.get('email')
        phone               = data.get('phone_number')
        gender              = data.get ('gender')
        full_name          = data.get('full_name')

        if phone and len(phone) != 10:
            raise serializers.ValidationError({'phone_number':'phone number must be 10 digits'})

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'passwords must match'})
        if len(password)<8:
            raise serializers.ValidationError({'password':'password must be atleast 8 charactera'})
        if password.isdigit():
            raise serializers.ValidationError({'password': 'password cannot be completely numerical'})

        user_info = ['username','email','phone_number','full_name','last_name']
        if any(info and info.lower() == password.lower() for info in user_info):
            raise serializers.ValidationError({'password':'password cannot contain any of the user information'})
        
        return data
    
    def create(self,validated_data):
        validated_data.pop('confirm_password') #Remove confirm_password from the validated_data and keep only password
        plane_password = validated_data['password']

        validated_data['password'] = make_password(plane_password)

        user = User.objects.create(**validated_data)

        return user
        
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)

    class Meta:
        model = User
        fields = ['username','password']


class UserLogoutSerializers(serializers.Serializer):
    refresh  = serializers.CharField()

    default_error_messages = {
        'bad_token':'Token is expired or invalid'
    }

    def validate(self,attrs):
        self.token = attrs['refresh']

        return attrs
    
    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')




    


