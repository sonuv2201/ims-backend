from cProfile import Profile
from uuid import uuid4
from rest_framework import serializers
from django.contrib.auth.models import Group, User

from .models import (
    ChangePasswordModel,
    EntityPermission,
    Grouping,
    GroupingEntityPermission,
    GroupUser,
    Entity,
    FooterConfiguration,
    GenericUser,
    AdminMenu,
    HeaderConfiguration,
    HeaderFooterModel,
    LCNCManagement,
    MetaConfiguration,
    ResetPasswordModel,
    Sidebar,
)

from django.apps import apps

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime, timedelta
from pytz import timezone

from django.urls import get_resolver, URLPattern, URLResolver, reverse, NoReverseMatch
from django.conf import settings
import json


def get_named_endpoints():
    resolver = get_resolver()
    named_endpoints = []
    excluded_paths = [
        "/",
        "/generic-api/entities/",
        "/generic-api/users/",
        "/generic-api/groups/",
        "/generic-api/groups-entity-permissions/",
        "/generic-api/groups-entity-permissions/available_entities/",
        "/generic-api/groups-user/",
        "/generic-api/admin-menus/",
        "/generic-api/entities-permission/",
        "/generic-api/access-control/",
        "/api/refresh-token/",
        "/auth/configuration/",
        "/noauth/api/login-via-email/password/",
        "/noauth/api/reset/password/email/",
        "/noauth/api/reset/password/email/otp/",
        "/lcnc-management/",
    ]

    try:
        with open("excluded_paths.json", "r") as file:
            json_excluded_paths = json.load(file)
            if isinstance(json_excluded_paths, list):
                excluded_paths.extend(json_excluded_paths)
            else:
                raise ValueError("JSON file must contain a list of paths.")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading excluded paths from JSON: {e}")

    def recursive_url_parser(urlpatterns, parent_pattern=""):
        for url in urlpatterns:
            if isinstance(url, URLPattern) and url.name:
                try:
                    path = reverse(url.name)
                    # Only add endpoints not in the excluded list
                    if path not in excluded_paths:
                        named_endpoints.append((path, path))
                except NoReverseMatch:
                    continue
            elif isinstance(url, URLResolver):
                recursive_url_parser(
                    url.url_patterns, parent_pattern + str(url.pattern)
                )

    recursive_url_parser(resolver.url_patterns)

    return named_endpoints


class GroupingEntityPermissionSerializer(serializers.ModelSerializer):
    Group = serializers.PrimaryKeyRelatedField(queryset=Grouping.objects.all())

    class Meta:
        model = GroupingEntityPermission
        fields = [
            "Group",
            "entity_name",
            "table_name",
            "columns",
            "can_create",
            "can_read",
            "can_update",
            "can_delete",
        ]


class EntitySerializer(serializers.ModelSerializer):
    model_name = serializers.ChoiceField(choices=[])

    class Meta:
        model = Entity
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch all registered models in the project
        model_choices = [
            (model._meta.label, model._meta.label)  # (app.ModelName, app.ModelName)
            for model in apps.get_models()
        ]

        # Set the choices dynamically for the model_name field
        self.fields["model_name"].choices = model_choices


# class GenericUserSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True, style={"input_type": "password"})
#     Group = serializers.CharField(source="Group.name", read_only=True)

#     class Meta:
#         model = GenericUser
#         fields = "__all__"


class GenericUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    # Group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())  # Shows ID-based selection
    # Group = serializers.CharField(source="Group.name", read_only=True)

    class Meta:
        model = GenericUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "Group",
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the Group model."""

    parent = serializers.PrimaryKeyRelatedField(
        queryset=Grouping.objects.all(),  # All available Groupings for parent selection
        required=False,
        allow_null=True,
    )
    # users = UserSerializer(many=True, read_only=True)  # Nested user details
    # sub_groups = serializers.StringRelatedField(
    #     many=True, read_only=True
    # )  # Display sub-department names

    class Meta:
        model = Grouping
        fields = ["id", "name", "parent"]

    def to_representation(self, instance):
        """Customize the output to show a readable name for 'parent'."""
        data = super().to_representation(instance)
        if instance.parent:
            data["parent"] = instance.parent.name

        data["sub_groups"] = [
            {"id": sub_group.id, "name": sub_group.name}
            for sub_group in instance.sub_groups.all()
        ]

        return data


class GroupUserSerializer(serializers.ModelSerializer):
    """Serializer for the intermediate GroupUser model."""

    user = UserSerializer()  # Nested user details
    Group = serializers.StringRelatedField()  # Display Group name

    class Meta:
        model = GroupUser
        fields = ["id", "Group", "user", "assigned_at", "role"]


from rest_framework import serializers
from django.urls import get_resolver
from .models import AdminMenu


class AdminMenuSerializer(serializers.ModelSerializer):
    """Serializer for AdminMenu with dynamic 'entity' choices."""

    entity = serializers.ChoiceField(choices=[])  # Dynamic choices for 'entity'

    class Meta:
        model = AdminMenu
        fields = "__all__"

    def __init__(self, *args, **kwargs):

        self.fields["entity"].choices = get_named_endpoints()

        super().__init__(*args, **kwargs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        """
        This method generates a customized refresh token and access token.
        """
        token = super().get_token(user)

        # Clear all default fields from the token payload
        token.payload.clear()

        # Add custom claims to the token payload
        token["jti"] = str(uuid4())
        token["token_type"] = "refresh"
        token["login"] = True
        token["id"] = user.id
        token["user_id"] = user.id
        token["username"] = user.email  # Assuming username is used
        token["expire_by"] = (
            datetime.now(timezone("Asia/Kolkata")) + timedelta(minutes=60)
        ).isoformat()

        token["exp"] = (
            datetime.now(timezone("Asia/Kolkata")) + timedelta(minutes=15)
        ).timestamp()

        return token

    def validate(self, attrs):
        """
        Ensures the access and refresh tokens are returned as strings.
        """
        data = super().validate(attrs)

        # Generate customized refresh token
        refresh = self.get_token(self.user)

        # Create a separate access token with its `type` claim
        access = refresh.access_token
        access["type"] = "access"  # Indicate this is an access token

        # Extract and assign customized tokens
        data["access"] = str(access)
        data["refresh"] = str(refresh)

        # Add optional extra fields to the response payload if needed
        data["username"] = self.user.email
        data["user_id"] = self.user.id

        return data


class SidebarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sidebar
        fields = "__all__"


class MetaConfigurationSerializer(serializers.ModelSerializer):
    sidebar = SidebarSerializer()

    class Meta:
        model = MetaConfiguration
        fields = "__all__"


class HeaderConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderConfiguration
        fields = "__all__"


class FooterConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterConfiguration
        fields = "__all__"


class HeaderFooterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderFooterModel
        fields = "__all__"


class LCNCManagementSerializer(serializers.ModelSerializer):
    meta = MetaConfigurationSerializer()
    header = HeaderConfigurationSerializer()
    footer = FooterConfigurationSerializer()

    class Meta:
        model = LCNCManagement
        fields = ["meta", "header", "footer"]

    def create(self, validated_data):
        # Extract meta, header, and footer data from validated_data
        meta_data = validated_data.pop("meta")
        header_data = validated_data.pop("header")
        footer_data = validated_data.pop("footer")

        # Create Sidebar if provided in meta
        sidebar_data = meta_data.pop("sidebar", None)
        sidebar = Sidebar.objects.create(**sidebar_data) if sidebar_data else None

        # Create MetaConfiguration
        meta = MetaConfiguration.objects.create(**meta_data, sidebar=sidebar)

        # Create HeaderConfiguration instance for header
        header_configuration = HeaderConfiguration.objects.create(**header_data)

        # Create FooterConfiguration instance for footer
        footer_configuration = FooterConfiguration.objects.create(**footer_data)

        # Create LCNCManagement instance and associate with header and footer
        lcnc_management = LCNCManagement.objects.create(
            meta=meta, header=header_configuration, footer=footer_configuration
        )

        return lcnc_management

    def update(self, instance, validated_data):
        # Extract meta, header, and footer data from validated_data
        meta_data = validated_data.pop("meta", None)
        header_data = validated_data.pop("header", None)
        footer_data = validated_data.pop("footer", None)

        # Update sidebar configuration if provided
        if meta_data and "sidebar" in meta_data:
            sidebar_data = meta_data.pop("sidebar")
            if instance.meta.sidebar:
                for attr, value in sidebar_data.items():
                    setattr(instance.meta.sidebar, attr, value)
                instance.meta.sidebar.save()
            else:
                instance.meta.sidebar = Sidebar.objects.create(**sidebar_data)
                instance.meta.save()

        # Update meta configuration if provided
        if meta_data:
            for attr, value in meta_data.items():
                setattr(instance.meta, attr, value)
            instance.meta.save()

        # Update header if provided
        if header_data:
            for attr, value in header_data.items():
                setattr(instance.header, attr, value)
            instance.header.save()

        # Update footer if provided
        if footer_data:
            for attr, value in footer_data.items():
                setattr(instance.footer, attr, value)
            instance.footer.save()

        # Update LCNCManagement instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    from django.urls import (
        get_resolver,
        URLPattern,
        URLResolver,
        reverse,
        NoReverseMatch,
    )


from rest_framework import serializers
from .models import EntityPermission


# Utility Function to Get Available Named Endpoints


class EntityPermissionSerializer(serializers.ModelSerializer):
    # entity = serializers.ChoiceField(choices=AVAILABLE_ENTITIES)
    entity = serializers.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        # Dynamically fetch available entities only when the serializer is instantiated
        self.fields["entity"].choices = get_named_endpoints()
        super().__init__(*args, **kwargs)

    class Meta:
        model = EntityPermission
        fields = "__all__"


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordModel
        fields = ["email"]  # Include all fields by default


class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangePasswordModel
        fields = "__all__"
