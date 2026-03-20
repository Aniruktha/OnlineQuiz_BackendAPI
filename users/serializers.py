from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    # Optional admin key to create admin users
    admin_key = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "admin_key"]

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password", "")
        admin_key = validated_data.get("admin_key", "")
        
        # Check if user already exists by username
        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)
            # Update email if different
            if user.email != email:
                user.email = email
                user.save()
            return user
        
        # Check if user exists by email
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            return user
        
        # Create new user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password if password else "default_password"
        )
        
        # First user becomes admin automatically OR with correct admin key
        secret_key = "admin_secret_key_123"
        if not CustomUser.objects.filter(is_staff=True).exists() or admin_key == secret_key:
            user.is_staff = True
            user.is_superuser = True
            user.role = "admin"
            user.save()
        
        return user