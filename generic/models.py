from django.db import models, IntegrityError
from django.utils import timezone
import uuid
from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAuthenticated


from generic.custom_model import GenericBaseModel

from django.db import models, connection
from django.db.models import Q
import os

from django.contrib.postgres.fields import ArrayField
from django.urls import get_resolver

from django.urls import get_resolver, URLPattern, URLResolver, reverse, NoReverseMatch


def upload_to_assets(instance, filename):
    """Generate upload path for files."""
    base, ext = os.path.splitext(filename)
    return f"assets/lcnc/{base}{ext}"


class SchemaManager(models.Manager):
    def get_metadata(self):
        query = """
        SELECT table_catalog, table_schema, table_name, table_type
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return [
                Schema(
                    table_catalog=row[0],
                    table_schema=row[1],
                    table_name=row[2],
                    table_type=row[3],
                )
                for row in results
            ]


class Schema(models.Model):
    table_catalog = models.CharField(max_length=255)  # Database name
    table_schema = models.CharField(max_length=255)  # Schema name (e.g., 'public')
    table_name = models.CharField(max_length=255)  # Table name
    table_type = models.CharField(max_length=255)  # Type (e.g., 'BASE TABLE', 'VIEW')

    objects = SchemaManager()

    class Meta:
        # Prevent migration
        managed = False
        # Descriptive name for the model
        verbose_name = "Information Schema"
        verbose_name_plural = "Information Schemas"

    def __str__(self):
        return f"{self.table_catalog}.{self.table_schema}.{self.table_name} ({self.table_type})"


class Entity(GenericBaseModel):
    entity_name = models.CharField(max_length=100)  # Define entity name
    model_name = models.CharField(
        max_length=100
    )  # Define model name for the permission

    def __str__(self):
        return f"{self.entity_name}"


class Grouping(GenericBaseModel):
    id = models.AutoField(primary_key=True)  # Explicit ID field
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_groups",
    )

    def __str__(self):
        return self.name


class GroupUser(GenericBaseModel):
    """
    Intermediate table for linking users to groups.
    """

    group = models.ForeignKey(
        Grouping, on_delete=models.CASCADE, related_name="group_users"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_groups")
    assigned_at = models.DateTimeField(default=timezone.now)  # Track assignment time
    role = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        help_text="Optional role of the user in this groups",
    )

    class Meta:
        unique_together = (
            "group",
            "user",
        )  # Prevent duplicate user-Group links

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class GroupingEntityPermission(GenericBaseModel):
    group = models.ForeignKey(
        "Grouping", on_delete=models.CASCADE, related_name="permissions"
    )
    entity_name = models.CharField(max_length=100)  # Represents the database entity
    table_name = models.CharField(max_length=100)  # New field for table name
    columns = ArrayField(
        models.CharField(max_length=100), blank=True, default=list
    )  # List of column names
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=True)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.Group.name} permissions for {self.entity_name} "
            f"(Table: {self.table_name}, Columns: {', '.join(self.columns)})"
        )


class Role(models.TextChoices):
    COMPANY = "COMPANY"
    AGENCY = "AGENCY"


class GenericUser(GenericBaseModel):
    class Meta:
        app_label = "generic"

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)

    Group = models.ForeignKey(
        Grouping, on_delete=models.SET_NULL, null=True, related_name="users"
    )


class AdminMenu(GenericBaseModel):
    TEMPLATE_CHOICES = [
        ("dashboard-generic-grid", "Dashboard Generic Grid"),
        ("default-home-page", "Default Home Page"),
        ("dashboard-generic-configuration", "Dashboard Generic Configuration"),
    ]

    template = models.CharField(
        max_length=255,
        choices=TEMPLATE_CHOICES,
        default="dashboard-generic-grid",  # Optional default value
    )

    label = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    entity = models.CharField(
        max_length=255,
    )
    icon = models.CharField(max_length=100)
    user_identifier = models.CharField(max_length=100)
    caches = models.BooleanField(default=False)
    key = models.CharField(max_length=255)
    order = models.IntegerField()
    hide = models.BooleanField(default=False)  # Add this line if missing

    def __str__(self):
        return self.label


class Sidebar(models.Model):
    logo = models.FileField(
        upload_to=upload_to_assets, blank=True, null=True
    )  # Upload for sidebar logo
    title = models.CharField(max_length=255, blank=True, null=True)
    is_title_hide = models.BooleanField(default=False)

    def __str__(self):
        return self.title or "Sidebar Configuration"


class MetaConfiguration(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    config_caches = models.BooleanField(default=True)
    copyright_text = models.CharField(max_length=255)
    login_logo = models.FileField(
        upload_to=upload_to_assets, blank=True, null=True
    )  # Upload for logo
    login_logo_width = models.IntegerField(default=100)
    login_logo_height = models.IntegerField(default=100)
    favicon = models.FileField(
        upload_to=upload_to_assets, blank=True, null=True
    )  # Upload for favicon
    sidebar_icon = models.FileField(
        upload_to=upload_to_assets, blank=True, null=True
    )  # Upload for sidebar icon
    sidebar_icon_width = models.IntegerField(default=100)
    sidebar_icon_height = models.IntegerField(default=100)
    default_auth = models.CharField(max_length=50)
    banner = models.FileField(
        upload_to=upload_to_assets, blank=True, null=True
    )  # Upload for banner
    banner_width = models.IntegerField(default=100)
    banner_height = models.IntegerField(default=100)
    is_banner_fulll_screen = models.BooleanField(default=False)
    banner_image_fill_type = models.CharField(max_length=50, null=True, blank=True)

    sidebar = models.OneToOneField(
        Sidebar,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="meta_sidebar",
    )

    def __str__(self):
        return self.title


class HeaderConfiguration(models.Model):
    template = models.CharField(max_length=50)
    entity = models.CharField(max_length=255)
    caches = models.BooleanField(default=False)

    def __str__(self):
        return self.template


class FooterConfiguration(models.Model):
    template = models.CharField(max_length=50)
    entity = models.CharField(max_length=255)
    caches = models.BooleanField(default=False)

    def __str__(self):
        return self.template


class HeaderFooterModel(models.Model):
    TYPE_CHOICES = [("header", "Header"), ("footer", "Footer"), ("layout", "Layout")]

    template = models.CharField(max_length=50)
    entity = models.CharField(max_length=255, blank=True, null=True)
    caches = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.get_type_display()} - {self.template}"


class LCNCManagement(GenericBaseModel):
    meta = models.OneToOneField(
        MetaConfiguration, on_delete=models.CASCADE, related_name="lcnc_meta"
    )
    header = models.OneToOneField(
        HeaderConfiguration,
        on_delete=models.CASCADE,
        related_name="lcnc_header",
    )
    footer = models.OneToOneField(
        FooterConfiguration,
        on_delete=models.CASCADE,
        related_name="lcnc_footer",
    )

    def get_default_extra():
        return {
            "form": {
                "title": "Entity",
                "description": None,
                "form_template": "form-template-two",
                "admin_menu_url": "",
                "entity": "/auth/configuration/",
                "size": {
                    "width": 50,
                    "height": "auto",
                    "maxWidth": 50,
                    "maxHeight": 80,
                },
                "column": {"desktop": 1, "laptop": 1, "tablet": 1},
                "gap": 4,
            }
        }

    extra = models.JSONField(default=get_default_extra)

    def __str__(self):
        return self.meta.title


class EntityPermission(GenericBaseModel):
    entity = models.CharField(max_length=255)
    group = models.ForeignKey(
        Grouping, on_delete=models.CASCADE, related_name="entity_permissions"
    )
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=True)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    # class Meta:
    #     unique_together = ("entity", "group")


class ResetPasswordModel(GenericBaseModel):
    email = models.EmailField()

    otp = models.CharField(max_length=10, null=True, blank=True)


class ChangePasswordModel(GenericBaseModel):
    email = models.EmailField()

    otp = models.CharField(max_length=10, null=True, blank=True)

    password = models.CharField(max_length=255, null=True, blank=True)
    confirm_password = models.CharField(max_length=255, null=True, blank=True)
