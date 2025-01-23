from rest_framework import serializers
from apps.user.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True)
    confirm_password =serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ['email','user_name','first_name','last_name','gender','phone_number','password','confirm_password','profile_image','department']
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


            return data
    


