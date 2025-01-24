from rest_framework import serializers
from apps.user.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    confirm_password =serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['email','user_name','first_name','gender','phone_number','password','confirm_password','profile_image','department']
        extra_kwargs = {
            'password' : {'write_only':True},
            'confirm_password' : {'write_only':True}
        }

        def validate(self,data):
            password            = data.get('password')
            confirm_password    = data.get('confirm_password')
            user_name           = data.get('user_name')
            email               = data.get('email')
            phone               = data.get('phone_number')
            gender              = data.get ('gender')
            first_name          = data.get('first_name')

            if password != confirm_password:
                raise serializers.ValidationError({'password': 'passwords must match'})
            if len(password)<8:
                raise serializers.ValidationError({'password':'password must be atleast 8 charactera'})
            if password.isdigit():
                raise serializers.ValidationError({'password': 'password cannot be completely numerical'})

            user_info = ['user_name','email','phone_number','first_name','last_name']
            if any(info and info.lower() == password.lower() for info in user_info):
                raise serializers.ValidationError({'password':'password cannot contain any of the user information'})
            
            return data
        
        def create(self,validated_data):
            validated_data.pop('confirm_password') #Remove confirm_password from the validated_data and keep only password
            plane_password = validated_data['password']

            validated_data['password'] = make_password(plane_password)
            user = User.objects.create(**validated_data)

            request = self.context['request']
            authenticated_user = authenticate(user_name=user.user_name,password=plane_password)
            if authenticated_user:
                login(request,authenticated_user)

            return user
    


