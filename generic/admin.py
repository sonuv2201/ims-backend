from django.contrib import admin
from .models import (
    Entity,
    Grouping,
    GroupingEntityPermission,
    GroupUser,
    EntityPermission,
)
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib.auth.models import Group, User


admin.register(Entity)
# class EntityPermissionAdmin(admin.ModelAdmin):
#     list_display = (
#         "entity_name",
#         "model_name",
#         "group",
#         "can_create",
#         "can_read",
#         "can_update",
#         "can_delete",
#     )
#     list_filter = ("group", "model_name")
#     search_fields = ("entity_name", "model_name")


# admin.site.register(Grouping)
# admin.site.register(GroupingEntityPermission)
class EntityPermissionResource(resources.ModelResource):
    class Meta:
        model = EntityPermission


@admin.register(EntityPermission)
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = EntityPermissionResource


# admin.site.register(EntityPermission)
admin.site.unregister(User)
# admin.site.unregister(Group)
