from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from superadmin.utils import generate_dashboard_config
from generic.models import (
    AdminMenu,
    EntityPermission,
    GenericUser,
    LCNCManagement,
)
from generic.serializers import AdminMenuSerializer, LCNCManagementSerializer
from generic.views import GenericModelViewSet, IsSuperAdminOrReadOnlyViewset
from superadmin.models import HomeModel
from superadmin.serializer import HomeModelSerializer
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework import permissions

from rest_framework.response import Response


import json

from django.db.models import Q

from rest_framework import serializers

from rest_framework.decorators import action

from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny


true, false, null = True, False, None


class HomeView(GenericModelViewSet):

    serializer_class = HomeModelSerializer

    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return HomeModel.objects.all()

    def options(self, request, *args, **kwargs):
        # Check if there are entries in the database
        self.queryset = self.get_queryset()
        if self.queryset.exists():
            # Extract dynamic data from the first entry
            first_entry = self.queryset.first()
            response = {
                "meta": {
                    "title": (
                        first_entry.title if first_entry.title else "Default Title"
                    ),
                    "description": (
                        first_entry.description
                        if first_entry.description
                        else "Default Description"
                    ),
                },
                "form": {
                    "title": (
                        first_entry.title if first_entry.title else "Default Title"
                    ),
                    "description": (
                        first_entry.description
                        if first_entry.description
                        else "Default Description"
                    ),
                    "form_template": (
                        first_entry.form_template
                        if first_entry.form_template
                        else "default-template"
                    ),
                    "entity": (
                        first_entry.entity if first_entry.entity else "/api/home/"
                    ),
                    "size": {
                        "width": first_entry.width if first_entry.width else 50,
                        "height": "auto",
                        "maxWidth": 50,
                        "maxHeight": 80,
                    },
                    "column": {"desktop": 1, "laptop": 1, "tablet": 1},
                    "gap": 4,
                },
                "actions": {
                    "view": {"label": "View", "icon": "eye"},
                    "edit": {"label": "Edit", "icon": "pencil", "inlineUpdate": False},
                    "delete": {"label": "Delete", "icon": "delete"},
                },
                "table": {"view": ["id"], "filter": {}},
                "layout": [
                    {
                        "template": "default-home-page",
                        "url": "/",
                        "entity": request.path,
                        "hostName": "crincit",
                        "api": [],
                    }
                ],
                "permissions": [],
                "POST": {
                    "create": {
                        "type": "button",
                        "required": True,
                        "read_only": False,
                        "label": "Submit",
                        "style": {
                            "align": "right",
                            "isFullWidth": True,
                            "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
                        },
                    }
                },
            }
        else:
            # Default response if no entries exist
            response = {
                "meta": {"title": "No Data", "description": "No entries available."},
                "form": {
                    "title": "Default Home",
                    "description": None,
                    "form_template": "default-template",
                    "entity": "/api/home/",
                    "size": {
                        "width": 50,
                        "height": "auto",
                        "maxWidth": 50,
                        "maxHeight": 80,
                    },
                    "column": {"desktop": 1, "laptop": 1, "tablet": 1},
                    "gap": 4,
                },
                "actions": {
                    "view": {"label": "View", "icon": "eye"},
                    "edit": {"label": "Edit", "icon": "pencil", "inlineUpdate": False},
                    "delete": {"label": "Delete", "icon": "delete"},
                },
                "table": {"view": ["id"], "filter": {}},
                "layout": [
                    {
                        "template": "default-home-page",
                        "url": "/",
                        "entity": request.path,
                        "hostName": "crincit",
                        "api": [
                            # {
                            #     "entity": request.path,
                            #     "method": "GET",
                            #     "apiKey": "get",
                            #     "isSearch": True,
                            #     "isDetails": True,
                            #     "localCacheName": "home-page",
                            #     "caches": True,
                            # }
                        ],
                    }
                ],
                "permissions": [],
                "POST": {
                    "create": {
                        "type": "button",
                        "required": True,
                        "read_only": False,
                        "label": "Submit",
                        "style": {
                            "align": "right",
                            "isFullWidth": True,
                            "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
                        },
                    }
                },
            }

        return Response(response, status=status.HTTP_200_OK)


class AuthConfigurationViewSet(GenericModelViewSet):
    queryset = LCNCManagement.objects.all()

    permission_classes = [AllowAny]

    serializer_class = LCNCManagementSerializer

    def check_permissions(self, request):
        return True

    def list(self, request, *args, **kwargs):
        # Get the queryset and serializer from the view
        user = request.user
        adminMenu = []

        if str(request.user) != "AnonymousUser":
            try:
                # Check if a User object exists first
                user_instance = User.objects.get(username=request.user.username)
                try:
                    # Fetch the corresponding GenericUser
                    generic_user = GenericUser.objects.get(
                        username=request.user.username
                    )

                    entity_permissions = EntityPermission.objects.filter(
                        group=generic_user.Group.id, can_read=True
                    )
                    print("Entity Permissions: ", entity_permissions)
                    accessible_entities = entity_permissions.values_list(
                        "entity", flat=True
                    )

                    adminMenu = [
                        generate_dashboard_config(a) for a in accessible_entities
                    ]
                except GenericUser.DoesNotExist:
                    print(
                        f"GenericUser for '{request.user}' not found in the database."
                    )
                    adminMenu = []
            except User.DoesNotExist:
                print(f"User '{request.user}' not found in the database.")
                adminMenu = []
        else:  # User is anonymous
            print("User is anonymous.")
            adminMenu = []

        lcnc_management = (
            LCNCManagement.objects.all()
            .select_related("meta", "meta__sidebar", "header", "footer")
            .first()
        )

        def absolute_url(relative_url):
            if relative_url:
                return request.build_absolute_uri(relative_url)
            return None

        # TODO: Add Logic to Add Banner to the Response banner_image
        # Check if the query result is empty
        if not lcnc_management:
            lcnc_management = {
                "meta": {
                    "title": "",
                    "description": "",
                    "config_caches": True,
                    "copyright_text": "",
                    "login_logo": None,
                    "sidebar_icon": None,
                    "default_auth": "",
                    "sidebar": {
                        "logo": None,
                        "title": "",
                        "isTitleHide": True,
                    },
                    "favicon": None,
                },
                "header": {
                    "template": "header-style-one",
                    "entity": "/dashboard/management",
                    "caches": False,
                },
                "footer": {
                    "template": "footer-style-one",
                    "entity": "/dashboard/management",
                    "caches": False,
                },
            }
        else:
            # Manually structure the data into the desired JSON format
            lcnc_management = {
                "meta": {
                    "title": lcnc_management.meta.title,
                    "description": lcnc_management.meta.description,
                    "config_caches": lcnc_management.meta.config_caches,
                    "copyright_text": lcnc_management.meta.copyright_text,
                    "login_logo": (
                        absolute_url(lcnc_management.meta.login_logo.url)
                        if lcnc_management.meta.login_logo
                        else None
                    ),
                    "login_logo_width": lcnc_management.meta.login_logo_width,
                    "login_logo_height": lcnc_management.meta.login_logo_height,
                    "favicon": (
                        absolute_url(lcnc_management.meta.favicon.url)
                        if lcnc_management.meta.favicon
                        else None
                    ),
                    "sidebar_icon": (
                        absolute_url(lcnc_management.meta.sidebar_icon.url)
                        if lcnc_management.meta.sidebar_icon
                        else None
                    ),
                    "sidebar_icon_width": lcnc_management.meta.sidebar_icon_width,
                    "sidebar_icon_height": lcnc_management.meta.sidebar_icon_height,
                    "default_auth": lcnc_management.meta.default_auth,
                    "banner": (
                        absolute_url(lcnc_management.meta.banner.url)
                        if lcnc_management.meta.banner
                        else None
                    ),
                    "banner_width": lcnc_management.meta.banner_width,
                    "banner_height": lcnc_management.meta.banner_height,
                    "sidebar": {
                        "logo": (
                            absolute_url(lcnc_management.meta.sidebar.logo.url)
                            if lcnc_management.meta.sidebar.logo
                            else None
                        ),
                        "title": lcnc_management.meta.sidebar.title,
                        "isTitleHide": lcnc_management.meta.sidebar.is_title_hide,
                    },
                },
                "header": {
                    "template": lcnc_management.header.template,
                    "entity": lcnc_management.header.entity,
                    "caches": lcnc_management.header.caches,
                },
                "footer": {
                    "template": lcnc_management.footer.template,
                    "entity": lcnc_management.footer.entity,
                    "caches": lcnc_management.footer.caches,
                },
            }

        response = {
            **lcnc_management,
            "adminMenu": adminMenu,
            "siteMenu": [
                {
                    "template": "coming-soon",
                    "label": "Home",
                    "url": "/",
                    "entity": "/api/home/",
                    "icon": "page",
                    "id": "excel_sheet",
                    "caches": True,
                    "local": true,
                    "key": "excel_sheet",
                }
            ],
            "authMenu": {
                "login_with_email": [
                    {
                        "template": "login-template-one",
                        "label": "Sign in",
                        "url": "/auth/login",
                        "entity": "/noauth/api/login-via-email/password/",
                        "id": "login-email-password",
                        "keepToken": true,
                        "caches": true,
                    }
                ],
                "login_with_email_otp": [
                    {
                        "template": "login-template-one",
                        "label": "Sign in",
                        "url": "/auth/login-with-email-otp",
                        "entity": "/noauth/api/login-via-email/",
                        "id": "login-email",
                        "caches": true,
                        "nextPage": "/auth/login/verify-otp",
                        "param": "email",
                    },
                    {
                        "template": "login-template-one",
                        "label": "Sign in",
                        "url": "/auth/login/verify-otp",
                        "entity": "/noauth/api/verify-otp/",
                        "id": "login-email-verify-otp",
                        "keepToken": true,
                        "caches": true,
                        "prevParam": "email",
                    },
                ],
                "login_with_mobile_otp": [],
                "reset_password": [
                    {
                        "template": "login-template-one",
                        "label": "Reset Password",
                        "url": "/auth/forgot-password-email",
                        "entity": "/noauth/api/reset/password/email/",
                        "id": "reset-email-password",
                        "caches": true,
                        "nextPage": "/auth/reset-email-otp-password",
                        "param": "email",
                    },
                    {
                        "template": "login-template-one",
                        "label": "Sign in",
                        "url": "/auth/reset-email-otp-password",
                        "entity": "/noauth/api/reset/password/email/otp/",
                        "id": "reset-email-password-otp",
                        "keepToken": true,
                        "caches": true,
                        "prevParam": "email",
                    },
                ],
            },
        }

        return Response(response)


class LCNCManagementViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = LCNCManagement.objects.all()
    serializer_class = LCNCManagementSerializer

    def partial_update(self, request, *args, **kwargs):
        # Use the DRF-provided `partial=True` flag
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        current_options = super().options(request, *args, **kwargs)
        current_options.data["layout"][0][
            "template"
        ] = "dashboard-generic-configuration"

        return current_options
