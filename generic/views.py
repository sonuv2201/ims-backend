import re
from rest_framework import filters
from django.contrib.auth.models import Group
from django.db import ProgrammingError, connection

from superadmin.models import HomeModel
from superadmin.serializer import HomeModelSerializer
from .models import (
    AdminMenu,
    ChangePasswordModel,
    EntityPermission,
    GroupingEntityPermission,
    GroupUser,
    Entity,
    GenericUser,
    LCNCManagement,
    ResetPasswordModel,
    Schema,
    User,
    Group,
    Grouping,
)

from django.http import JsonResponse
from .serializers import (
    AdminMenuSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    EntityPermissionSerializer,
    GroupingEntityPermissionSerializer,
    GroupUserSerializer,
    EntitySerializer,
    LCNCManagementSerializer,
    ResetPasswordSerializer,
    UserSerializer,
    GroupSerializer,
    GroupSerializer,
    GenericUserSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework import permissions

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied, NotFound

from rest_framework.decorators import action
from collections import defaultdict

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status

import json

from django.db.models import Q

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import serializers
from django.urls import reverse, NoReverseMatch
from django.urls import get_resolver

from django.urls import get_resolver, URLPattern, URLResolver, reverse, NoReverseMatch
from django.core.mail import send_mail
import random
from django.contrib.auth.hashers import make_password


true, false, null = True, False, None


class HomePageView(APIView):
    def get(self, request):
        """
        Return all available clean URLs across the Django project.
        """

        # Return clean data
        data = {
            "message": "Welcome to the NISH!",
            "redirect_to": "http://localhost:3000/",
        }
        return Response(data, status=status.HTTP_200_OK)


class CustomPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = "per_page"  # Allows dynamic page size
    max_page_size = 100  # Optional: Prevents abuse

    def paginate_queryset(self, queryset, request, view=None):
        # Update self.page_size dynamically
        per_page = request.query_params.get(self.page_size_query_param)
        if per_page and per_page.isdigit():
            self.page_size = int(per_page)

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "per_page": self.page_size,  # Now properly updated
                "previous": self.get_previous_link(),
                "next": self.get_next_link(),
                "response": data,
            }
        )


class GenericModelViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        """
        Override to add custom permission checks based on EntityPermission.
        """
        # Map actions to permissions
        if re.match(r"^/noauth/", request.path):
            return True

        if request.user.is_superuser:
            return True

        action_permission_map = {
            "list": "can_read",
            "retrieve": "can_read",
            "create": "can_create",
            "update": "can_update",
            "partial_update": "can_update",
            "destroy": "can_delete",
            "options": "can_read",
        }

        # Get the current action
        action = self.action

        # Skip permissions for safe methods
        if action not in action_permission_map:
            return super().check_permissions(request)

        # Retrieve the logged-in user

        try:
            user = GenericUser.objects.filter(username=request.user).first()
            if not user:
                raise ValueError("User not found.")

            # Retrieve the user's group
            group = Grouping.objects.filter(id=user.Group.id).first()
            if not group:
                raise ValueError("Group not found.")

            cleaned_path = re.sub(r"/\d+/?$", "/", request.path)

            # Retrieve the current entity permission
            entity_permission = EntityPermission.objects.filter(
                group=group, entity=cleaned_path
            ).first()

            if not entity_permission:
                raise PermissionDenied("You do not have access to this resource.")

            # Check if the user has permission for the current action
            has_permission = getattr(
                entity_permission, action_permission_map[action], False
            )
        except ValueError as e:
            print(f"Error: {e}")
            has_permission = False
        if not has_permission:
            raise PermissionDenied(f"Permission denied for {action} action.")

    # def check_permissions(self, request):
    #     """
    #     Override to add custom permission checks based on EntityPermission.
    #     """
    #     # Map actions to permissions
    #     if re.match(r"^/noauth/", request.path):
    #         return True

    #     if request.user.is_superuser:
    #         return True

    #     action_permission_map = {
    #         "list": "can_read",
    #         "retrieve": "can_read",
    #         "create": "can_create",
    #         "update": "can_update",
    #         "partial_update": "can_update",
    #         "destroy": "can_delete",
    #         "options": "can_read",
    #     }

    #     # Get the current action
    #     action = self.action

    #     # Skip permissions for safe methods
    #     if action not in action_permission_map:
    #         return super().check_permissions(request)

    #     # Retrieve the logged-in user

    #     try:
    #         user = GenericUser.objects.filter(username=request.user).first()
    #         if not user:
    #             raise ValueError("User not found.")

    #         # Retrieve the user's group
    #         group = Grouping.objects.filter(id=user.Group.id).first()
    #         if not group:
    #             raise ValueError("Group not found.")

    #         # Retrieve the current entity permission
    #         entity_permission = EntityPermission.objects.filter(
    #             group=group, entity=request.path
    #         ).first()

    #         if not entity_permission:
    #             raise PermissionDenied("You do not have access to this resource.")

    #         # Check if the user has permission for the current action
    #         has_permission = getattr(
    #             entity_permission, action_permission_map[action], False
    #         )
    #     except ValueError as e:
    #         print(f"Error: {e}")
    #         has_permission = False
    #     if not has_permission:
    #         raise PermissionDenied(f"Permission denied for {action} action.")

    def options(self, request, *args, **kwargs):

        self.check_permissions(request)
        # Get the serializer instance
        serializer = self.get_serializer()

        # Get the model name dynamically from the serializer's Meta class
        if self.queryset:
            model_name = self.queryset.model._meta.verbose_name.title() or "Entity"
        else:
            model_name = "Entity"  # Default value if queryset is None

        api_title = getattr(self, "name", model_name)

        # Construct the 'actions' metadata dynamically
        type_map = {
            "IntegerField": "integer",
            "PrimaryKeyRelatedField": "choice",  # ForeignKey as choice
            "RelatedField": "choice",
            "DateTimeField": "date",
            "CharField": "string",
            "BooleanField": "boolean",
            "JSONField": "JSONField",
            "ManyRelatedField": "array",
            "ListSerializer": "array",
            "URLField": "string",
            "ChoiceField": "choice",
            "EmailField": "email",
            "FloatField": "float",
            "SlugRelatedField": "choice",
        }
        hidden_fields = {"id", "updated_at", "created_at", "extra"}

        def get_serializer_metadata(
            serializer, hidden_fields=None, type_map=None, prefix=""
        ):
            if hidden_fields is None:
                hidden_fields = []
            if type_map is None:
                type_map = {}

            actions_metadata = {}

            if isinstance(serializer, serializers.ListSerializer):
                serializer = serializer.child  # Use the child serializer for fields

            for field_name, field in serializer.fields.items():
                # Full field name with prefix for flat structure
                full_field_name = f"{prefix}{field_name}" if prefix else field_name

                # Determine the field type
                field_type_name = type(field).__name__
                if (
                    field_type_name == "CharField"
                    and field.style.get("input_type") == "password"
                ):
                    field_type = "password"
                else:
                    field_type = type_map.get(field_type_name, field_type_name)

                # Check if the field is a serializer (nested serializer)
                if isinstance(field, serializers.BaseSerializer):
                    # Recursively get metadata for nested serializer with prefixed names
                    nested_metadata = get_serializer_metadata(
                        field, hidden_fields, type_map, prefix=f"{full_field_name}."
                    )
                    # Add all nested fields to the flat structure
                    actions_metadata.update(nested_metadata)
                else:
                    # Handle simple fields
                    actions_metadata[full_field_name] = {
                        "type": field_type,
                        "required": field.required,
                        "read_only": field.read_only,
                        "label": field.label,
                        "max_length": getattr(field, "max_length", None),
                        "choices": [
                            {"display_name": value, "value": key}
                            for key, value in getattr(field, "choices", {}).items()
                        ],
                        "placeholder": getattr(field, "placeholder", ""),
                        "hidden": full_field_name in hidden_fields,
                    }

            return actions_metadata

        actions_metadata = get_serializer_metadata(serializer, hidden_fields, type_map)

        actions_metadata["create"] = {
            "type": "button",
            "required": True,
            "read_only": False,
            "label": "Submit",
            "style": {
                "align": "right",
                "isFullWidth": True,
                "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
            },
            "button_style": "login",
        }
        actions_metadata["detail"] = {
            "type": "error",
        }
        # Additional UI and layout configurations
        template_name = "form-template-one"
        # breakpoint()
        form = {
            "title": model_name,
            "description": None,
            "form_template": template_name,
            "entity": request.path,  # Endpoint path
            "size": {
                "width": 50,
                "height": "auto",
                "maxWidth": 50,
                "maxHeight": 80,
            },
            "column": {
                "desktop": 1,
                "laptop": 1,
                "tablet": 1,
            },
            "gap": 4,
        }

        api_mapping = {
            "list": {
                "method": "GET",
                "apiKey": "get",
                "isSearch": True,
                "isDetails": False,
            },
            # "retrieve": {
            #     "method": "GET",
            #     "apiKey": "details",
            #     "isSearch": False,
            #     "isDetails": True,
            # },
            # "create": {
            #     "method": "POST",
            #     "apiKey": "create",
            #     "isSearch": False,
            #     "isDetails": False,
            # },
            # "update": {
            #     "method": "PUT",
            #     "apiKey": "update",
            #     "isSearch": False,
            #     "isDetails": True,
            # },
            # "destroy": {
            #     "method": "DELETE",
            #     "apiKey": "delete",
            #     "isSearch": False,
            #     "isDetails": False,
            # },
        }

        # Constructing the `api` list dynamically
        api_list = [
            {
                "entity": request.path,
                "method": config["method"],
                "apiKey": config["apiKey"],
                "isSearch": config["isSearch"],
                "isDetails": config["isDetails"],
            }
            for config in api_mapping.values()
        ]

        layout = [
            {
                "template": "dashboard-generic-grid",
                "detailsTemplate": "dashboard-generic-list-details",
                "url": request.path,
                "entity": request.path,
                "api": api_list,
            }
        ]

        def merge_dicts(existing, new):
            for key, value in new.items():
                if key in existing:
                    if isinstance(existing[key], dict) and isinstance(value, dict):
                        # Recursive merge for nested dictionaries
                        merge_dicts(existing[key], value)
                    elif isinstance(existing[key], list) and isinstance(value, list):
                        # Merge lists by appending unique items
                        existing[key].extend(x for x in value if x not in existing[key])
                    else:
                        # For non-dict or non-list values, overwrite with new value
                        existing[key] = value
                else:
                    # Add new key-value pair
                    existing[key] = value

        # Query and merge all `extra` options from the table
        extra_options = defaultdict(dict)

        if request.path != "/noauth/api/login-via-email/password/":
            if hasattr(self.queryset.model, "extra"):
                extras = self.queryset.model.objects.values_list("extra", flat=True)
                for extra in extras:
                    if isinstance(extra, str):
                        # Handle JSON strings
                        try:
                            extra_dict = json.loads(extra)
                        except json.JSONDecodeError:
                            print("Invalid JSON:", extra)  # Debugging invalid JSON
                            continue
                    elif isinstance(extra, dict):
                        # Handle dictionaries directly
                        extra_dict = extra
                    else:
                        print(
                            "Unsupported extra format:", extra
                        )  # Debugging unsupported format
                        continue

                    # Merge the extra dictionary into `extra_options`
                    merge_dicts(extra_options, extra_dict)

        # Convert defaultdict to a regular dictionary
        extra_options = dict(extra_options)

        # Permissions from the Entity model
        group = request.user.groups.first()

        if not group:
            # Handle users with no group assigned
            print("No group assigned to the user.")  # Debugging output
            group_permissions = []
        else:
            # Safely fetch group permissions
            group_permissions = group.permissions.all()
        http_methods = set()

        try:
            # Attempt to fetch the user
            user = GenericUser.objects.filter(username=request.user).first()
            if not user:
                raise ValueError("User not found.")

            # Attempt to fetch the user's group
            group = Grouping.objects.filter(id=user.Group.id).first()
            if not group:
                raise ValueError("Group not found.")

            # Attempt to fetch the entity permission for the group and request path
            current_entity = EntityPermission.objects.filter(
                group=group, entity=request.path
            ).first()
            if not current_entity:
                raise ValueError("Entity permissions not found for the current entity.")

            # Map entity permissions to HTTP methods
            permission_to_http_methods = {
                "can_create": ["post"],
                "can_update": ["put", "patch"],
                "can_delete": ["delete"],
                "can_read": ["get", "options"],
            }

            # Collect allowed HTTP methods based on entity permissions
            if current_entity.can_create:
                http_methods.update(permission_to_http_methods["can_create"])
            if current_entity.can_update:
                http_methods.update(permission_to_http_methods["can_update"])
            if current_entity.can_delete:
                http_methods.update(permission_to_http_methods["can_delete"])
            if current_entity.can_read:
                http_methods.update(permission_to_http_methods["can_read"])

            # Convert to a sorted list for consistent output
            http_methods = sorted(http_methods)

            # Optional mapping for table actions
            http_method_to_table_action = {
                "get": "view",
                "patch": "edit",
                "delete": "delete",
            }

        except ValueError as e:
            print(f"Error: {e}")
        except AttributeError as e:
            print(f"AttributeError encountered: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")
        # Debugging output

        predefined_table_actions = {
            "view": {"label": "View", "icon": "eye"},
            "edit": {"label": "Edit", "icon": "pencil", "inlineUpdate": False},
            "delete": {"label": "Delete", "icon": "delete"},
            "create": {"label": "Create", "icon": "plus"},  # Optional action
        }

        table_actions = {
            action: predefined_table_actions[action]
            for method in http_methods
            if (action := http_method_to_table_action.get(method))
            in predefined_table_actions
        }
        # Dynamic table configurations

        serializer = self.get_serializer()

        # Get the model from the serializer's Meta class
        # Fetch the model from serializer metadata
        model = getattr(serializer.Meta, "model", None)

        if model:
            # Dynamically get field names from the model
            field_array = [
                field.name
                for field in model._meta.fields
                if field.name not in hidden_fields  # Exclude hidden fields
            ]
        else:
            # Default to an empty array if no model is found
            field_array = []

        # Fetch distinct values for each field
        def fetch_column_values(field):
            try:
                # Use the ORM to get distinct values for the field
                return list(model.objects.values_list(field, flat=True).distinct())
            except Exception as e:
                # Handle cases where fetching values might fail
                print(f"Error fetching values for field '{field}': {e}")
                return []

        # Construct the filter dictionary dynamically
        filter_config = {
            field: {
                "search_url": f"/api/search/{field}",  # Example endpoint pattern
                "values": fetch_column_values(field),  # Fetch actual distinct values
            }
            for field in field_array
        }

        # Final table configuration
        table = {
            "view": field_array,  # Dynamic columns populated above
            "filter": filter_config,  # Dynamic filters with actual values populated here
        }
        # if self.queryset:
        #     field_array = [
        #         field.name
        #         for field in self.queryset.model._meta.fields
        #         if field.name not in hidden_fields  # Exclude hidden fields
        #     ]
        #     print(field_array)
        # else:
        #     field_array = []

        # table = {
        #     "view": field_array,  # Dynamic columns populated above
        #     "filter": {},  # Add filter options if required
        # }

        # table_actions = {
        #     "view": {"label": "View", "icon": "eye"},
        #     "edit": {"label": "Edit", "icon": "pencil", "inlineUpdate": false},
        #     "delete": {"label": "delete", "icon": "delete"},
        # }
        # breakpoint()

        # Merged data response
        data = {
            "meta": {
                "title": "Nish",
                "description": f"",
            },
            "form": form,
            "actions": table_actions,  # Add dynamic action metadata here if required
            "table": table,
            "layout": layout,
            "permissions": http_methods,
            "POST": actions_metadata,
            **extra_options,
        }

        # Merge `extra_options` with the `data`
        # merge_dicts(data, extra_options)

        return Response(data)

    def create(self, request, *args, **kwargs):
        # Create logic remains the same
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Ensure pagination after creation (if needed)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

        # queryset = self.get_queryset()
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return self.get_paginated_response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search = self.request.GET.get("_gq", "")
        if search:
            query = Q()
            model_fields = [
                field.name
                for field in queryset.model._meta.get_fields()
                if field.is_relation is False  # Exclude relational fields
            ]

            # Split search terms by comma
            search_terms = [term.strip() for term in search.split(",") if term.strip()]
            for term in search_terms:
                field_queries = Q()
                for field in model_fields:
                    try:
                        # Check if the field is CharField or TextField
                        field_type = queryset.model._meta.get_field(
                            field
                        ).get_internal_type()
                        if field_type in ["CharField", "TextField"]:
                            field_queries |= Q(**{f"{field}__icontains": term})
                    except FieldDoesNotExist:
                        continue  # Skip invalid fields
                query |= field_queries

            queryset = queryset.filter(query)

        # Filtering functionality
        filtering_params = (
            self.request.GET.dict()
        )  # Get all query parameters as a dictionary
        reserved_keys = ["search", "sort_by", "sort_order"]  # Reserved keys to skip
        filter_conditions = {
            key: value
            for key, value in filtering_params.items()
            if key not in reserved_keys
        }

        if filter_conditions:
            query = Q()
            for field, value in filter_conditions.items():
                if hasattr(
                    queryset.model, field
                ):  # Ensure the field exists in the model
                    query &= Q(**{f"{field}": value})  # Exact match filtering
            queryset = queryset.filter(query)

        # Sorting functionality
        sort_by = self.request.GET.get("sort_by", None)  # Column to sort by
        sort_order = self.request.GET.get("sort_order", "asc")  # "asc" or "desc"
        if sort_by:
            if hasattr(queryset.model, sort_by):  # Check if the sorting field exists
                sort_field = f"-{sort_by}" if sort_order == "desc" else sort_by
                queryset = queryset.order_by(sort_field)
            else:
                raise ValueError(f"Invalid sort field: {sort_by}")

        return queryset

    def list(self, request, *args, **kwargs):
        # Check for permission using has_permission
        self.check_permissions(request)

        # Use the queryset and serializer from the view
        queryset = self.filter_queryset(self.get_queryset())

        # Search functionality (dynamically search across fields)
        search_query = request.query_params.get("_gq", None)

        if search_query:
            search_fields = getattr(self.serializer_class.Meta, "search_fields", [])
            if search_fields:
                query = Q()
                for field in search_fields:
                    query |= Q({f"{field}__icontains": search_query})
                queryset = queryset.filter(query)

        # Sorting functionality
        sort_by = request.query_params.get("sort_by", None)  # Column to sort by
        sort_order = request.query_params.get("sort_order", "asc")  # "asc" or "desc"

        if sort_by:
            if sort_order == "desc":
                queryset = queryset.order_by(f"-{sort_by}")  # Descending order
            else:
                queryset = queryset.order_by(sort_by)  # Ascending order

        # Handle "no_paginate" case
        no_paginate = request.query_params.get("no_paginate", None)
        if no_paginate:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Pagination
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)

        if paginated_queryset is not None:
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        # If no pagination, return the entire queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     # Check for permission using `has_permission`
    #     self.check_permissions(request)

    #     # Use the queryset and serializer from the view
    #     queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)

    #     # Search functionality (dynamically search across fields)
    #     search_query = request.query_params.get("_gq", None)

    #     no_paginate = request.query_params.get("no_paginate", None)
    #     if no_paginate:
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)

    #     if search_query:
    #         search_fields = getattr(self.serializer_class.Meta, "search_fields", [])
    #         if search_fields:
    #             query = Q()
    #             for field in search_fields:
    #                 query |= Q(**{f"{field}__icontains": search_query})
    #             queryset = queryset.filter(query)

    #     # Sorting functionality
    #     sort_by = request.query_params.get("sort_by", None)  # Column to sort by
    #     sort_order = request.query_params.get("sort_order", "asc")  # "asc" or "desc"

    #     if sort_by:
    #         if sort_order == "desc":
    #             queryset = queryset.order_by(f"-{sort_by}")  # Descending order
    #         else:
    #             queryset = queryset.order_by(sort_by)  # Ascending order

    #     # Pagination (if needed)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     # If no pagination, return the entire queryset
    #     serializer = self.get_serializer(queryset, many=True)
    #     return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Check for permission using `has_permission`
        self.check_permissions(request)

        # Retrieve the object using the provided pk or kwargs
        try:
            instance = self.get_object()
        except Exception:
            raise NotFound(detail="Object not found")

        # Serialize the object
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        # Similar to your existing update logic with pagination
        self.check_permissions(request)
        try:
            instance = self.get_object()
        except Exception:
            raise NotFound(detail="Object not found")

        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # After update, return the paginated data
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Fallback to non-paginated response if pagination is not applied
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        # Retrieve the instance to be updated
        self.check_permissions(request)
        try:
            instance = self.get_object()  # Get the instance from the URL lookup
        except Entity.DoesNotExist:
            raise NotFound(detail="Object not found", code=status.HTTP_404_NOT_FOUND)

        # Update the serializer with the instance and partial data
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        # Validate the serializer (this step ensures that only valid data is passed)
        serializer.is_valid(raise_exception=True)

        # Save the updated instance and return a response
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)

        return super().destroy(request, *args, **kwargs)

    def get_paginated_response(self, data):
        """
        Custom pagination response.
        """
        paginator = PageNumberPagination()
        paginator.page_size = self.request.query_params.get(
            "per_page", 5
        )  # Default to 5 per page
        paginator.queryset = self.get_queryset()
        paginated_data = paginator.paginate_queryset(paginator.queryset, self.request)

        return Response(
            {
                "count": paginator.page.paginator.count,
                "per_page": paginator.page_size,
                "previous": paginator.get_previous_link(),
                "next": paginator.get_next_link(),
                "response": data,
            }
        )


class CustomTokenObtainPairView(GenericModelViewSet):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get_queryset(self):
        """
        This viewset does not use a queryset because it handles authentication.
        """
        return None

    def list(self, request, *args, **kwargs):
        """
        This viewset does not use a queryset because it handles authentication.
        """
        return Response({"message": "This endpoint does not support listing."})

    def options(self, request, *args, **kwargs):
        """
        Handle the OPTIONS request to customize the response.
        """
        # Create a custom response
        custom_options = {
            "meta": {"title": "Login", "description": ""},
            "form": {
                "title": "Email Login",
                "description": null,
                "form_template": "form-template-one",
                "entity": "/noauth/api/login-via-email/password/",
                "size": {
                    "width": 50,
                    "height": "auto",
                    "maxWidth": 50,
                    "maxHeight": 80,
                },
                "column": {"desktop": 1, "laptop": 1, "tablet": 1},
                "gap": 4,
            },
            "actions": {},
            "table": {
                "view": [
                    "heading",
                    "sub_heading",
                    "email",
                    "password",
                    "divider",
                    "other_login_options",
                    "id",
                ],
                "filter": {},
            },
            "layout": [
                {
                    "template": "auth-style-one",
                    "url": "/login",
                    "entity": "/noauth/api/login-via-email/password/",
                    "api": [],
                }
            ],
            "permissions": [],
            "POST": {
                "heading": {
                    "type": "heading",
                    "label": "Welcome Back",
                    "className": "mb-[-16px]",
                    "style": {"align": "center"},
                    "hidden": True,
                },
                "sub_heading": {
                    "type": "description",
                    "label": "Please sign in to continue",
                    "className": "mb-8",
                    "style": {"align": "center"},
                    "hidden": True,
                },
                "username": {
                    "type": "string",
                    "read_only": false,
                    "label": "Enter your email",
                    "required": true,
                    "max_length": 100,
                    "icon": "email",
                    "label_hidden": true,
                    "placeholder": "Username",
                },
                "password": {
                    "type": "password",
                    "read_only": false,
                    "label": "Password:",
                    "required": true,
                    "max_length": 100,
                    "icon": "password",
                    "label_hidden": true,
                    "placeholder": "Password",
                },
                # "forget_password": {
                #     "type": "link",
                #     "required": false,
                #     "hidden": false,
                #     "read_only": false,
                #     "style": {
                #         "align": "right",
                #         "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
                #     },
                #     "content": [
                #         {
                #             "link": "/auth/forgot-password-email",
                #             "text": "Forgot Password?",
                #             "target": "_self",
                #         }
                #     ],
                #     "inputType": "secondary",
                # },
                "create": {
                    "type": "button",
                    "required": true,
                    "read_only": false,
                    "label": "Login",
                    "style": {
                        "align": "right",
                        "isFullWidth": true,
                        "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
                    },
                    "button_style": "login",
                },
                # "divider": {
                #     "type": "divider",
                #     "style": "type-1",
                #     "label": "or Sign-in with",
                #     "label_hidden": true,
                # },
                # "other_login_options": {
                #     "type": "other_login_options",
                #     "style": "type-1",
                #     "content": {
                #         "login_with_email_otp": {
                #             "label": "Email Otp",
                #             "url": "/auth/login-with-email-otp",
                #             "icon": "Mail",
                #         }
                #     },
                # },
            },
        }

        return Response(custom_options)

    # Override the create method to handle POST requests
    def create(self, request, *args, **kwargs):
        """
        Handle POST requests for authentication.
        """
        token_view = TokenObtainPairView.as_view(serializer_class=self.serializer_class)
        response = token_view(
            request._request, *args, **kwargs
        )  # Pass the original WSGIRequest

        if response.status_code == 200:
            data = response.data
            user = User.objects.get(id=data["user_id"])
            custom_data = {
                "message": "Verification successful",
                "token": data.get("access"),
                "refresh_token": data.get("refresh"),
                "password_reset": True,
                "password_reset_url": None,
                "is_admin": user.is_superuser,
                "role": None,
            }
            return Response(custom_data, status=response.status_code)
        return response


class IsSuperAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only superadmins to perform unsafe methods
    (e.g., POST, PUT, DELETE) while allowing all authenticated users to read (GET).
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Allow read-only access for authenticated users
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        # Allow superadmins to perform unsafe actions
        return request.user.is_superuser


class IsSuperAdminOrReadOnlyViewset(
    GenericModelViewSet,
):
    permission_classes = [IsSuperAdminOrReadOnly]


class GroupingEntityPermissionsViewSet(IsSuperAdminOrReadOnlyViewset):
    """
    ViewSet for managing Group-based permissions.
    """

    # queryset = GroupEntityPermission.objects.all()
    serializer_class = GroupingEntityPermissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter the queryset by Group if the `Group` query parameter is provided.
        """
        queryset = GroupingEntityPermission.objects.all()
        Group = self.request.query_params.get("Group", None)

        if Group:
            queryset = queryset.filter(
                Group=Group
            )  # Adjust this according to your model field

        return queryset

    @action(detail=False, methods=["get"])
    def available_entities(self, request):
        """
        Returns a list of available entities and their columns from the Schema table.
        """
        try:
            with connection.cursor() as cursor:
                # Query table names and columns from information_schema.columns
                cursor.execute(
                    """
                    SELECT table_name, column_name
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    ORDER BY table_name, ordinal_position
                    """
                )
                rows = cursor.fetchall()

                # Transform rows into the desired format
                entities = {}
                for table_name, column_name in rows:
                    if table_name not in entities:
                        entities[table_name] = []
                    entities[table_name].append(column_name)

        except ProgrammingError as e:
            # Handle case where the query fails
            return Response({"error": str(e)}, status=500)

        return Response(entities)


class EntityViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class UserViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = GenericUser.objects.all()
    serializer_class = GenericUserSerializer

    def create(self, request, *args, **kwargs):
        # Create logic remains the same
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user, created = User.objects.get_or_create(
            username=request.data["username"],
            defaults={
                "email": request.data["email"],
                "is_superuser": False,
                "is_staff": False,
            },
        )
        if created:
            user.set_password(request.data["password"])
            user.save()
            print(f"user '{request.data["username"]}' created.")
        else:
            print(f"user '{request.data["username"]}' already exists.")

        # Add user to the given group
        group_name = Grouping.objects.get(id=request.data["Group"]).name

        print(f"Group '{group_name}' found.")

        # Ensure pagination after creation (if needed)
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update all fields of the GenericUser and corresponding Django User models except is_superuser and is_staff."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        # Update GenericUser
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update corresponding Django User
        user = User.objects.get(username=instance.username)
        user.email = request.data.get("email", user.email)
        if "password" in request.data:
            user.set_password(request.data["password"])
        user.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """Update selected fields of the GenericUser and corresponding Django User models."""
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete the GenericUser and its corresponding Django User."""
        instance = self.get_object()

        # Delete GenericUser
        self.perform_destroy(instance)

        # Delete corresponding Django User
        try:
            user = User.objects.get(username=instance.username)
            user.delete()
            print(f"user '{instance.username}' deleted.")
        except User.DoesNotExist:
            print(
                f"user '{instance.username}' does not exist in the Django User model."
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class NoPagination(PageNumberPagination):
    page_size = None  # This disables pagination
    page_size_query_param = "page_size"
    max_page_size = 1000  # Adjust this based on your use case


class GroupingViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = Grouping.objects.all()
    serializer_class = GroupSerializer


class AdminMenuViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = AdminMenu.objects.all()
    serializer_class = AdminMenuSerializer


class GroupUserViewSet(IsSuperAdminOrReadOnlyViewset):
    """
    ViewSet for managing GroupUser objects.
    """

    queryset = GroupUser.objects.select_related("group", "user").all()
    serializer_class = GroupUserSerializer


class CustomTokenRefreshView(TokenRefreshView):
    def get(self, request, *args, **kwargs):
        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return Response(
                {"detail": "Authorization header must contain Bearer token."},
                status=400,
            )

        # Extract the token value
        token = auth_header.split(" ")[1]
        try:
            serializer = self.get_serializer(data={"refresh": token})
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # Extract validated data and include the original refresh token
        validated_data = serializer.validated_data
        access_token = validated_data.get("access")

        # Return the customized response
        return Response(
            {
                "token": access_token,
                "refresh_token": token,  # Include the original refresh token
            }
        )


class EntityPermissionViewset(IsSuperAdminOrReadOnlyViewset):
    queryset = EntityPermission.objects.all()
    serializer_class = EntityPermissionSerializer


class AccessControlViewSet(IsSuperAdminOrReadOnlyViewset):
    queryset = HomeModel.objects.all()
    serializer_class = HomeModelSerializer

    # def options(self, request, *args, **kwargs):
    #     if (
    #         request.user.is_authenticated and request.user.is_superuser
    #     ) or request.user.is_staff:
    #         response = {
    #             "meta": {
    #                 "title": "Access Control",
    #                 "description": "No entries available.",
    #             },
    #             "permissions": [],
    #             "layout": [
    #                 {
    #                     "template": "access-controls-template",
    #                     "url": "/dashboard/access-control",
    #                     "entity": "/generic-api/access-control/",
    #                     "hostName": "crincit",
    #                     "api": [],
    #                 }
    #             ],
    #         }

    #         return Response(response)

    #     else:
    #         return Response(
    #             {"message": "You are not authorized to access this resource."},
    #             status=status.HTTP_403_FORBIDDEN,
    #         )


class ResetPasswordViewset(GenericModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ResetPasswordModel.objects.all()
    serializer_class = ResetPasswordSerializer

    def options(self, request, *args, **kwargs):
        response = {
            "meta": {"title": "", "description": ""},
            "form": {
                "title": "Forgot Password Email",
                "description": null,
                "form_template": "form-template-one",
                "entity": "/noauth/api/reset/password/email/",
                "size": {
                    "width": 50,
                    "height": "auto",
                    "maxWidth": 50,
                    "maxHeight": 80,
                },
                "column": {"desktop": 1, "laptop": 1, "tablet": 1},
                "gap": 4,
            },
            "actions": {},
            "table": {
                "view": ["heading", "email", "forget_password", "id"],
                "filter": {},
            },
            "layout": [
                {
                    "template": "auth-style-two",
                    "url": "/auth/forgot-password-email",
                    "entity": "/noauth/api/reset/password/email/",
                    "api": [],
                }
            ],
            "permissions": [],
            "POST": {
                "heading": {
                    "type": "heading",
                    "label": "Forgot password",
                    "className": "mb-[10px]",
                    "style": {"align": "left"},
                },
                "email": {
                    "type": "email",
                    "read_only": false,
                    "label": "Enter your email",
                    "required": true,
                    "max_length": 100,
                    "icon": "email",
                    "label_hidden": true,
                    "placeholder": "Email",
                },
                "create": {
                    "type": "button",
                    "required": true,
                    "read_only": false,
                    "label": "Send OTP",
                    "className": "mt-0 pb-0",
                    "style": {
                        "align": "right",
                        "isFullWidth": true,
                        "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
                    },
                    "button_style": "login",
                },
                "forget_password": {
                    "type": "link",
                    "required": false,
                    "hidden": false,
                    "read_only": false,
                    "style": {
                        "align": "left",
                        "colMerge": {"deskTop": 1, "tablet": 1, "mobile": 1},
                    },
                    "content": [
                        {
                            "link": "/auth/login",
                            "text": "Remember password?",
                            "target": "_self",
                        }
                    ],
                    "inputType": "secondary",
                },
            },
        }

        return Response(response)

    def create(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)

        # Save the OTP and email in the model (assuming you have a field for this in ResetPasswordModel)
        ResetPasswordModel.objects.create(email=email, otp=otp)

        # Send the OTP to the user's email
        try:
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is: {otp}",
                from_email="noreply@example.com",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"error": "Failed to send email", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return the response
        return Response(
            {"message": "Otp Send successfully", "next_page": "noauth/verify-otp/"},
            status=status.HTTP_200_OK,
        )


class ChangePasswordViewset(GenericModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = ChangePasswordModel.objects.all()
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        # Retrieve email, OTP, and passwords from the request data
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        # Validate required fields
        if not email or not otp or not password or not confirm_password:
            return Response(
                {"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if passwords match
        if password != confirm_password:
            return Response(
                {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the email exists in the User model
        if not User.objects.filter(email=email).exists():
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate OTP from ResetPasswordModel
        try:
            reset_entry = ResetPasswordModel.objects.get(email=email, otp=otp)
        except ResetPasswordModel.DoesNotExist:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Hash the password before saving
        hashed_password = make_password(password)

        # Update password for the Django default User model
        try:
            user = User.objects.get(email=email)
            user.password = hashed_password
            user.save()

            # If using a custom user model, update the password here as well
            if hasattr(user, "genericusermodel"):  # Check for related custom user model
                generic_user = user.genericusermodel
                generic_user.password = hashed_password
                generic_user.save()
        except User.DoesNotExist:
            return Response(
                {"error": "User not found in the default User model"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the OTP entry after successful password change
        reset_entry.delete()

        # Return success response
        return Response(
            {"message": "Password changed successfully", "next_page": "noauth/login/"},
            status=status.HTTP_200_OK,
        )
