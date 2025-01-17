from rest_framework import serializers
from user.models import User, Role, AuthToken


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("uuid", "name")
        read_only_fields = ("uuid",)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    def get_role(self, instance):
        # ug = instance.groups.filter().last()
        # if not ug:
        #     return
        # return RoleSerializer(ug).data
        return

    def get_last_login(self, instance):
        auth_token = (
            AuthToken.objects.filter(user=instance).order_by("-issued_at").last()
        )
        if not auth_token:
            return None
        return auth_token.issued_at

    class Meta:
        model = User
        fields = (
            "uuid",
            "full_name",
            "email",
            "role",
            "last_login",
            "is_active",
            "created_at",
        )
        read_only_fields = ("id", "last_login", "created_at")


class UserWriteSerializer(UserSerializer):
    role = serializers.IntegerField(write_only=True)
    password = serializers.CharField(required=False, allow_null=True, write_only=True)

    def validate_role(self, data):
        role = Group.objects.filter(id=data).last()
        if not role:
            raise serializers.ValidationError("Invalid role")
        return role

    def validate(self, attrs):
        instance = self.instance
        validated_data = super().validate(attrs)
        username = validated_data.get("username")
        if not instance:
            if not validated_data["password"]:
                raise serializers.ValidationError(
                    {"password": "this field is required"}
                )

            exists_email = User.objects.filter(username=username)
        else:
            exists_email = User.objects.filter(username=username).exclude(
                id=instance.id
            )

        if exists_email:
            raise serializers.ValidationError(
                {"username": "has already exists. Please pick another one."}
            )

        return validated_data

    def create(self, validated_data):
        group = validated_data.pop("role")
        password = validated_data.pop("password", None)

        # Create File instance
        user_instance = User.objects.create(**validated_data)
        if password:
            user_instance.set_password(password)
        user_instance.groups.set([group])
        user_instance.save()

        return user_instance

    def update(self, user_instance, validated_data):
        group = validated_data.pop("role", None)
        password = validated_data.pop("password", None)

        if password:
            user_instance.set_password(password)

        if group:
            user_instance.groups.set([group])

        for attr, value in validated_data.items():
            setattr(user_instance, attr, value)
        user_instance.save()
        return user_instance

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("password",)
