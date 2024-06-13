from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import serializers
from . models import User, FriendRequestModel



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()

        # Check if passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        # Remove password2 from validated data
        validated_data.pop('password2')

        # Normalize email to lowercase
        validated_data['email'] = validated_data['email'].lower()

        # Create the user with the validated data
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # Set the user's password
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email').lower()  # Normalize the email to lowercase
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email address.')

        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')

        if not user.is_active:
            raise serializers.ValidationError('User is not active.')

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return data
    

class FriendRequestSerializer(serializers.ModelSerializer):
    to_user_email = serializers.EmailField(write_only=True)

    class Meta:
        model = FriendRequestModel
        fields = ['id', 'to_user_email', 'status', 'timestamp']
        read_only_fields = ['from_user', 'to_user', 'status', 'timestamp']

    def validate_to_user_email(self, value):
        try:
            to_user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return to_user

    def create(self, validated_data):
        to_user = validated_data.pop('to_user_email')
        from_user = self.context['request'].user
        friend_request = FriendRequestModel.objects.create(from_user=from_user, to_user=to_user)
        return friend_request
    
class RespondFriendRequestSerializer(serializers.ModelSerializer):
    to_user = serializers.EmailField()

    class Meta:
        model = FriendRequestModel
        fields = ['status', 'to_user']

    def validate_to_user(self, value):
        try:
            receiver = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return receiver

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.to_user = validated_data.get('to_user', instance.to_user)
        instance.save()
        return instance
    
class FriendRequestSerializerDisplay(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequestModel
        fields = ['id', 'from_user', 'to_user', 'status', 'timestamp']

    def get_from_user(self, obj):
        return obj.from_user.username if obj.from_user else None

    def get_to_user(self, obj):
        return obj.to_user.username if obj.to_user else None
    

class FriendRequestSerializerDisplay(serializers.ModelSerializer):
    from_user = RegisterSerializer()
    to_user = RegisterSerializer()

    class Meta:
        model = FriendRequestModel
        fields = ['id', 'from_user', 'to_user', 'status']