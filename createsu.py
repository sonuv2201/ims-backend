import os
import django
import random
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nish.settings")


# Initialize Django
django.setup()


from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from generic.models import Grouping, GenericUser


def random_string(length=8):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


# Replace 'myproject.settings' with your Django project settings

print("Welcome to the Django superuser and group creation script.")
print("Please Select one of following Options:")
# print("1. Create Superuser")
# print("2. Exit")

# option = input("Enter your choice: ")


# if option == "1":
SUPERUSER_USERNAME = input("Enter superuser username: ")
SUPERUSER_EMAIL = input("Enter superuser email: ")
SUPERUSER_PASSWORD = input("Enter superuser password: ")

# if option == "2":
#     exit()

GROUP_NAME = "Group"


def create_superuser_and_group():
    try:
        # Create or retrieve superuser
        superuserGroup = {
            "id": 2,
            "name": "Superuser",
            "parent": None,
        }

        grouping, created = Grouping.objects.update_or_create(
            id=superuserGroup["id"],
            defaults=superuserGroup,  # Update fields if the record already exists
        )
        if created:
            print(f"Created new entry: {grouping.name}")
        else:
            print(f"Updated existing entry: {grouping.name}")

        user = {
            "username": SUPERUSER_USERNAME,
            "email": SUPERUSER_EMAIL,
            "password": SUPERUSER_PASSWORD,
            "first_name": "Super",
            "last_name": "User",
            "Group": grouping,
        }

        genericUser, created = GenericUser.objects.update_or_create(
            username=user["username"],
            defaults=user,  # Update fields if the record already exists
        )

        superuser, created = User.objects.get_or_create(
            username=SUPERUSER_USERNAME,
            defaults={"email": SUPERUSER_EMAIL, "is_superuser": True, "is_staff": True},
        )
        if created:
            superuser.set_password(SUPERUSER_PASSWORD)
            superuser.save()
            print(f"Superuser '{SUPERUSER_USERNAME}' created.")
        else:
            print(f"Superuser '{SUPERUSER_USERNAME}' already exists.")

        # Create or retrieve group

        group, created = Group.objects.get_or_create(name=GROUP_NAME)
        if created:
            print(f"Group '{GROUP_NAME}' created.")
        else:
            print(f"Group '{GROUP_NAME}' already exists.")

        # Assign permissions to the group
        permissions = Permission.objects.all()
        group.permissions.set(permissions)
        group.save()
        print(f"All permissions added to group '{GROUP_NAME}'.")

        # Add superuser to the group
        superuser.groups.add(group)
        print(f"Superuser '{SUPERUSER_USERNAME}' added to group '{GROUP_NAME}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    create_superuser_and_group()
