from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from .models import User

def validate_password(password):
    
    if len(password)<6:
        pwreason = ('password must be greater than or equal to 6 characters')
        return '',pwreason
    
    if len(password)>16:
        pwreason = ('password must be less than or equal to 16 characters')
        return '',pwreason
    return password,''

class SignUpSerializer(serializers.ModelSerializer):
    '''Serializer for Signing up'''
    password = serializers.CharField(max_length=16, min_length=6,
                                     write_only=True)

    class Meta:
        model = User
        fields = ['email','password']
        

    def validate(self, attrs):
        
        password = attrs.get('password', '')
        email= attrs.get('email','').lower()
        user = User.objects.filter(email=email)
        
        #Checking if user is already registered
        if user:
            raise serializers.ValidationError({'error': 'Email already registered !'})
        
        password,error2=validate_password(password)

        if len(password)==0:
            raise serializers.ValidationError(error2)
        
            
        return attrs
    def create(self, validated_data): 
        user = User.objects.create_user(**validated_data)
        return user 
    


#Log in serializer
class LogInSerializer(serializers.ModelSerializer):
    '''Serializer for Log in'''
    email = serializers.EmailField(max_length=60)

    
    password = serializers.CharField(max_length=16, min_length=6,
                                     write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']
        read_only_fields = ['tokens']
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        email=email.lower()
        user = auth.authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed('Invalid email or password.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        # if not user.is_verified:
        #     raise AuthenticationFailed('Email is not verified')
        # exist= Desire.objects.filter(name="غزل ونسيج", uid=1, order=1,owner=user)  
        # if not exist:  
        #     Desire.objects.create(name="غزل ونسيج", uid=1, order=1,owner=user)
        #     Desire.objects.create(name="ميكانيكا انتاج", uid=2, order=2,owner=user)
        #     Desire.objects.create(name="ميكانيكا اجهزة", uid=3, order=3,owner=user)
        #     Desire.objects.create(name="كهرباء تحكم آلى", uid=4, order=4,owner=user)
        #     Desire.objects.create(name="كهرباء الكترونيات", uid=5, order=5,owner=user)
        #     Desire.objects.create(name="عمارة", uid=6, order=6,owner=user)
        #     Desire.objects.create(name="مدنى", uid=7, order=7,owner=user)
        return {
            'email': user.email,
            'tokens': user.tokens
        }
