import os
import django

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nish.settings")

# Initialize Django
django.setup()

from generic.models import AdminMenu, EntityPermission, Grouping
from generic.models import Entity
from superadmin.models import HomeModel

true, false = True, False
grouping = Grouping.objects.get(id=2)


entity_permission = [
    {
        "id": 2,
        "entity": "/lcnc-management/",
        "can_create": true,
        "can_read": true,
        "can_update": true,
        "can_delete": true,
        "group": grouping,
    },
    {
        "id": 5,
        "entity": "/generic-api/users/",
        "can_create": true,
        "can_read": true,
        "can_update": true,
        "can_delete": true,
        "group": grouping,
    },
    {
        "id": 16,
        "entity": "/generic-api/access-control/",
        "can_create": true,
        "can_read": true,
        "can_update": true,
        "can_delete": true,
        "group": grouping,
    },
    {
        "id": 17,
        "entity": "/generic-api/groups/",
        "can_create": true,
        "can_read": true,
        "can_update": true,
        "can_delete": true,
        "group": grouping,
    },
]

# Create or update entries in the database
for entry in entity_permission:
    entity_permission, created = EntityPermission.objects.update_or_create(
        id=entry["id"],
        defaults=entry,  # Update fields if the record already exists
    )
    if created:
        print(f"Created new entry: {entity_permission.entity}")
    else:
        print(f"Updated existing entry: {entity_permission.entity}")


homemodel, created = HomeModel.objects.update_or_create(
    title="Access Control",
    description="No entries available.",
    form_template="access-controls-template",
    entity="/generic-api/access-control/",
    width=12,
    extra={
        "meta": {
            "title": "Access Control",
            "description": "No entries available.",
        },
        "permissions": [],
        "layout": [
            {
                "template": "access-controls-template",
                "url": "/dashboard/access-control",
                "entity": "/generic-api/access-control/",
                "hostName": "crincit",
                "api": [],
            }
        ],
    },
)

if created:
    print(f"Created new entry: {homemodel.title}")
