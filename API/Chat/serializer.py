from rest_framework import serializers,validators
from .models import ChatAdmin
from django.contrib.auth.hashers import make_password

class ChatAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatAdmin
        fields = ['username', 'email', 'password']

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "allow_blank": False,
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        ChatAdmin.objects.all(), "A user with that Email already registered"
                    )
                ]
            }

        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        

        hashed_password = make_password(password)
        user = ChatAdmin.objects.create(
            password=hashed_password, **validated_data)
        
        return user
        # else:
        #     raise serializers.ValidationError({
        #         'error':'passwords do  not match'
        #     })
