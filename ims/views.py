from django.db.models import Q
from django.shortcuts import render
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from generic.views import GenericModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView


from ims.models import (
    Salesman,
    Company,
    CustomerType,
    PaymentTerms,
    CustomerGroup,
    ProductionPromotion,
    Customer,
    PricingModel,
    PricingAndTax,
    ShippingBillingAddress,
    SecInformation,
    Vendor,
    PurchaseOrder,
    Item,
    PurchaseOrderItem,
    GoodsInward,
    GoodsInwardItem,
    Inventory,
    InventoryItem,
    GoodsReceipt,
    GoodsReceiptItem,
    Employee,
    Expense,
    CustomerInformation,
    SalesOrder,
    ItemInformation,
    OrderHistory,
    System,
    CustomerDetails,
    ItemCategory,
    ItemDetails,
    Invoice,
    InvoiceItem,
    InvoiceHistory,
    InvoiceType,
    Brand,
    UPC,
    SecItemInformation,
    ItemTax,
    ItemCash,
    MSAInformation,
    VendorSecondaryInformation,
    VendorShippingBillingAddress,
    # Country,
    # ZipCode,
    # City,
    State,
    Tax,
    Department,
    ItemPrice,
    ItemVendor,
    CustomerSpecialPricing,
    SpecialPricingClassification,
    ItemSecondaryCategory,
)

from ims.serializers import (
    SalesmanSerializer,
    CompanySerializer,
    CustomerTypeSerializer,
    PaymentTermsSerializer,
    CustomerGroupSerializer,
    ProductionPromotionSerializer,
    CustomerSerializer,
    PricingModelSerializer,
    PricingAndTaxSerializer,
    ShippingBillingAddressSerializer,
    SecInformationSerializer,
    VendorSerializer,
    PurchaseOrderSerializer,
    ItemSerializer,
    PurchaseOrderItemSerializer,
    GoodsInwardSerializer,
    GoodsInwardItemSerializer,
    InventorySerializer,
    InventoryItemSerializer,
    GoodsReceiptSerializer,
    GoodsReceiptItemSerializer,
    EmployeeSerializer,
    ExpenseSerializer,
    CustomerInformationSerializer,
    SalesOrderSerializer,
    ItemInformationModelSerializer,
    OrderHistorySerializer,
    SystemSerializer,
    CustomerDetailsSerializer,
    ItemCategorySerializer,
    ItemSecondaryCategorySerializer,
    ItemDetailsSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    InvoiceHistorySerializer,
    InvoiceTypeSerializer,
    BrandSerializer,
    UPCModelSerializer,
    ItemTaxSerializer,
    SecItemSerializer,
    ItemCashSerializer,
    MSAInformationSerializer,
    VendorSecondaryInformationSerializer,
    VendorShippingBillingAddressSerializer,
    # CountrySerializer,
    # ZipCodeSerializer,
    # CitySerializer,
    StateSerializer,
    TaxSerializer,
    DepartmentSerializer,
    ItemPriceSerializer,
    ItemVendorSerializer,
    CustomerSpecialPricingSerializer,
    SpecialPricingClassificationSerializer,
    SpecialItemPriceSerializer,
)

options = {
    "meta": {"title": "", "description": ""},
    "form": {"title": ""},
    "actions": {},
    "table": {},
    "layout": [{"template": "dashboard-coming-soon", "api": []}],
    "permissions": [],
    "POST": {},
}

vendor_tab = [
    {
        "label": "Create Vendor",
        "isFirstTab": True,
        "key": "create-vendor",
        "type": "vendor",
        "entity": "/api/create-vendor/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Secondary Information",
        "isFirstTab": False,
        "key": "vendor-sec-information",
        "type": "vendor",
        "entity": "/api/vendor-sec-information/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Shipping Billing Address",
        "isFirstTab": False,
        "key": "vendor-shipping-billing-address",
        "type": "vendor",
        "entity": "/api/vendor-shipping-billing-address/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
]


customer_tab = [
    {
        "label": "Account Information",
        "key": "account-information",
        "isFirstTab": True,
        "type": "customer",
        "entity": "/api/create-customer/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
        "auto_increment": "customer_code",
    },
    {
        "label": "Pricing & Tax",
        "key": "pricing-tax",
        "isFirstTab": False,
        "type": "customer",
        "entity": "/api/create-pricing-and-tax/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Shipping & Billing Address",
        "key": "shipping-billing-address",
        "isFirstTab": False,
        "type": "customer",
        "entity": "/api/create-shipping-billing-address/",
        "template": "tab-on-page-edit",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Sec Information",
        "key": "sec-information",
        "isFirstTab": False,
        "type": "customer",
        "entity": "/api/create-sec-information/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
]

item_tab = [
    {
        "label": "Item Information",
        "key": "add-items",
        "isFirstTab": True,
        "type": "item",
        "entity": "/api/add-items/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "UPC",
        "key": "item-upc",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-upc/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Sec Information",
        "key": "item-sec-information",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-sec-information/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Tax",
        "key": "item-tax",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-tax/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Cash",
        "key": "item-cash",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-cash/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Price",
        "key": "item-price",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-price/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "Vendor",
        "key": "item-vendor",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-vendor/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
    {
        "label": "MSA Information",
        "key": "item-msa-information",
        "isFirstTab": False,
        "type": "item",
        "entity": "/api/item-msa-information/",
        "template": "tab-create-only",
        "error_message": "First need to create Customer information",
    },
]


class CustomerSpecialPricingView(GenericModelViewSet):
    queryset = CustomerSpecialPricing.objects.all()
    serializer_class = CustomerSpecialPricingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_id = self.request.query_params.get("customer")

        if customer_id:
            try:
                customer_obj = Customer.objects.get(id=customer_id)
                customer_group = customer_obj.customer_group

                queryset = queryset.filter(
                    Q(customer_id=customer_id) | Q(customer_group=customer_group)
                )
            except Customer.DoesNotExist:
                queryset = queryset.none()

        return queryset


class SpecialPricingClassificationViewSet(GenericModelViewSet):
    queryset = SpecialPricingClassification.objects.all()
    serializer_class = SpecialPricingClassificationSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Customer Special Pricing"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "special-pricing-template"

        # Return the modified response
        return Response(original_data)


class SpecialPricingClassificationListingViewSet(GenericModelViewSet):
    queryset = SpecialPricingClassification.objects.all()
    serializer_class = SpecialPricingClassificationSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Customer Special Pricing"

        if "form" in original_data:
            original_data["form"]["button"] = {
                "label": "Add Customer Special Pricing group",
                "link": "/dashboard/customer-special-pricing",
            }

        # if "POST" in original_data:
        #     original_data["POST"]["update_price"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["is_expiration_date_apply"]["type"] = "hidden"
        if "POST" in original_data:
            original_data["POST"]["expire"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "view-only"

        # Return the modified response
        return Response(original_data)


class TaxViewSet(GenericModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Tax"
        if "form" in original_data:
            original_data["form"]["title"] = "Tax"
        if "POST" in original_data:
            original_data["POST"]["additional_tax"]["type"] = "radioButton"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class SearchTaxViewSet(GenericModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Tax"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


# class CountryViewSet(GenericModelViewSet):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
#     permission_classes = [AllowAny]


class SpecialItemPriceViewSet(GenericModelViewSet):
    queryset = ItemInformation.objects.all()
    serializer_class = SpecialItemPriceSerializer
    permission_classes = [AllowAny]


class StateViewSet(GenericModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "State"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


# class CityViewSet(GenericModelViewSet):
#     queryset = City.objects.all()
#     serializer_class = CitySerializer
#     permission_classes = [AllowAny]

#     def options(self, request, *args, **kwargs):
#         # Call the parent class's `options` method to get the default metadata
#         response = super().options(request, *args, **kwargs)
#         original_data = response.data  # Get the original data

#         # Ensure 'form' exists and update it with the new object
#         if "meta" in original_data:
#             original_data["meta"]["title"] = "City"
#         if "layout" in original_data:
#             original_data["layout"][0]["template"] = "on-page-edit"

#         # Return the modified response
#         return Response(original_data)


# class ZipCodeViewSet(GenericModelViewSet):
#     queryset = ZipCode.objects.all()
#     serializer_class = ZipCodeSerializer
#     permission_classes = [AllowAny]

#     def options(self, request, *args, **kwargs):
#         # Call the parent class's `options` method to get the default metadata
#         response = super().options(request, *args, **kwargs)
#         original_data = response.data  # Get the original data

#         # Ensure 'form' exists and update it with the new object
#         if "meta" in original_data:
#             original_data["meta"]["title"] = "Zip Code"
#         if "layout" in original_data:
#             original_data["layout"][0]["template"] = "on-page-edit"

#         # Return the modified response
#         return Response(original_data)


class SalesmanViewSet(GenericModelViewSet):
    queryset = Salesman.objects.all()
    serializer_class = SalesmanSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Salesman"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class CompanyNameViewSet(GenericModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Company Name"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class CustomerTypeViewSet(GenericModelViewSet):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Create Customer Type"
        if "POST" in original_data:
            original_data["POST"]["cash_and_carry_percentage"]["placeholder"] = ["0%"]
            original_data["POST"]["cash_and_carry_percentage"]["label"] = [
                "Cash and carry percentage (%)"
            ]
            original_data["POST"]["description"]["type"] = ["textarea"]
            original_data["POST"]["description"]["min_height"] = ["100px"]
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class BrandViewSet(GenericModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Create Brand"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class PaymentTermsViewSet(GenericModelViewSet):
    queryset = PaymentTerms.objects.all()
    serializer_class = PaymentTermsSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Payment Terms"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class CustomerGroupViewSet(GenericModelViewSet):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        if "meta" in original_data:
            original_data["meta"]["title"] = "Customer Group"
        if "POST" in original_data:
            original_data["POST"]["address"]["type"] = "google_address"

        if "form" in original_data:
            original_data["form"]["title"] = "Customer Group"

        # Return the modified response
        return Response(original_data)


class ProductionPromotionViewSet(GenericModelViewSet):
    queryset = ProductionPromotion.objects.all()
    serializer_class = ProductionPromotionSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Production Promotion"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class PricingModelViewSet(GenericModelViewSet):
    queryset = PricingModel.objects.all()
    serializer_class = PricingModelSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Pricing Model"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        if "POST" in original_data:
            original_data["POST"]["pricing_model_amount_type"]["type"] = "radioButton"

        # Return the modified response
        return Response(original_data)


class CustomerViewSet(GenericModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


# Customer Search page
class SearchCustomerViewSet(GenericModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object

        if "meta" in original_data:
            original_data["meta"]["title"] = "Search Customer"

        if "form" in original_data:
            original_data["form"]["button"] = {
                "label": "Add new customer",
                "link": "/dashboard/create-customer",
            }

        if "form" in original_data:
            original_data["form"]["other_config"] = {
                "customer_code": {
                    "required": False,
                },
                "customer_name": {
                    "required": False,
                },
                "contact_person_name": {
                    "hidden": "true",
                },
                "phone": {
                    "hidden": "hidden",
                },
                "email": {
                    "hidden": "true",
                },
                "fax": {
                    "hidden": "true",
                },
                "credit_limit": {
                    "hidden": "true",
                },
                "customer_note": {
                    "hidden": "true",
                },
                "is_active": {
                    "hidden": "true",
                },
                "is_msa_include": {
                    "hidden": "true",
                },
                "is_sales_tax_applicable": {
                    "hidden": "true",
                },
                "send_email_on_invoice_creation": {
                    "hidden": "true",
                },
                "salesman": {
                    "hidden": "true",
                },
                "customer_type": {
                    "required": False,
                },
                "company": {
                    "hidden": "true",
                },
                "payment_terms": {
                    "hidden": "true",
                },
                "customer_group": {
                    "hidden": "true",
                },
                "product_promotion": {
                    "hidden": "true",
                },
            }
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "view-only"

        # Return the modified response
        return Response(original_data)


class VendorViewSet(GenericModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]


class SearchVendorViewSet(GenericModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object

        if "meta" in original_data:
            original_data["meta"]["title"] = "Search Vendor"

        if "form" in original_data:
            original_data["form"]["button"] = {
                "label": "Add new vendor",
                "link": "/dashboard/create-vendor",
            }

        if "form" in original_data:
            original_data["form"]["other_config"] = {}
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "view-only"

        # Return the modified response
        return Response(original_data)


# Vendor Tab 1: Create Vendor
class CreateVendorViewSet(GenericModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key
        new_object = vendor_tab

        if "meta" in original_data:
            original_data["meta"]["title"] = "Vendor"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = new_object
        if "form" in original_data:
            original_data["form"]["dependency"] = "vendor"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "tab-layout-template"

        # Return the modified response
        return Response(original_data)


# Vendor Tab 2: Sec Vendor Info
class VendorSecViewSet(GenericModelViewSet):
    queryset = VendorSecondaryInformation.objects.all()
    serializer_class = VendorSecondaryInformationSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key
        new_object = vendor_tab

        if "meta" in original_data:
            original_data["meta"]["title"] = "Vendor Sec Information"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = new_object
        if "form" in original_data:
            original_data["form"]["dependency"] = "vendor"

        if "POST" in original_data:
            original_data["POST"]["vendor"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


# Vendor Tab 3: Shipping Billing Address
class VendorShippingBillingAddressViewSet(GenericModelViewSet):
    queryset = VendorShippingBillingAddress.objects.all()
    serializer_class = VendorShippingBillingAddressSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key
        new_object = vendor_tab

        if "meta" in original_data:
            original_data["meta"]["title"] = "Vendor Shipping Billing Address"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = new_object
        if "form" in original_data:
            original_data["form"]["dependency"] = "vendor"
        if "POST" in original_data:
            original_data["POST"]["vendor"]["type"] = "hidden"

        if "POST" in original_data:
            original_data["POST"]["address"]["type"] = "google_address"

        if "POST" in original_data:
            original_data["POST"]["address"]["schema"] = {
                "isStandalone": False,
                "autoPopulate": {
                    "state": "state",
                    "city": "city",
                    "city": "city",
                    "zip_code": "zip_code",
                    "country": "country",
                },
            }

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


# Customer Tab 1: Account Information
class CreateCustomerViewSet(GenericModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        if "meta" in original_data:
            original_data["meta"]["title"] = "Create Customer"
        if "form" in original_data:
            original_data["form"]["title"] = "Customer"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = customer_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "customer"

        if "POST" in original_data:
            original_data["POST"]["company"]["type"] = "multi_select"
        if "POST" in original_data:
            original_data["POST"]["customer_code"]["read_only"] = True

        # if "POST" in original_data:
        #     original_data["POST"]["customer_code"]["default_value"] = 1000
        if "POST" in original_data:
            original_data["POST"]["credit_limit"]["min_number"] = 1000
        if "POST" in original_data:
            original_data["POST"]["credit_limit"]["max_number"] = 1099999

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "tab-layout-template"

        # Return the modified response
        return Response(original_data)


# Item Tab 1: Add Item
class AddItemViewSet(GenericModelViewSet):
    queryset = ItemInformation.objects.all()
    serializer_class = ItemInformationModelSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        if "meta" in original_data:
            original_data["meta"]["title"] = "Add Item"

        if "form" in original_data:
            original_data["form"]["title"] = "Item"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "tab-layout-template"

        if "POST" in original_data:
            original_data["POST"]["item_dimension"]["type"] = "dimension"
        if "POST" in original_data:
            original_data["POST"]["item_dimension"]["order"] = 15
        if "POST" in original_data:
            original_data["POST"]["company"]["type"] = "multi_select"

        # Return the modified response
        return Response(original_data)


# Item Tab 2: Upc
class UpCViewSet(GenericModelViewSet):
    queryset = UPC.objects.all()
    serializer_class = UPCModelSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item UPC"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


# Item Tab 2: Second Information
class SecItemInformationViewSet(GenericModelViewSet):
    queryset = SecItemInformation.objects.all()
    serializer_class = SecItemSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item Sec Information"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        if "POST" in original_data:
            original_data["POST"]["system"]["type"] = "multi_select_pill"

        # Return the modified response
        return Response(original_data)


# Item Tab 3: Item Tax
class ItemTaxViewSet(GenericModelViewSet):
    queryset = ItemTax.objects.all()
    serializer_class = ItemTaxSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item tax Information"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        if "POST" in original_data:
            original_data["POST"]["taxable_by"]["type"] = "radioButton"
        if "POST" in original_data:
            original_data["POST"]["taxes"]["type"] = "table-list"
        if "POST" in original_data:
            original_data["POST"]["taxes"]["schema"] = {
                "endpoint": "/api/search-tax/",
                "label": "Add Tax",
            }
        if "POST" in original_data:
            original_data["POST"]["taxes"]["column_classes"] = "col-span_3"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


# Item Tab 3: Cash
class ItemCashViewSet(GenericModelViewSet):
    queryset = ItemCash.objects.all()
    serializer_class = ItemCashSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item Cash Information"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


# Item Tab 3: Price
class ItemPriceViewSet(GenericModelViewSet):
    queryset = ItemPrice.objects.all()
    serializer_class = ItemPriceSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item Price"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        # if "POST" in original_data:
        #     original_data["POST"]["prices"]["type"] = "price_input"

        # if "POST" in original_data:
        #     original_data["POST"]["prices"]["column_classes"] = "col-span_3"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "tab-coming-soon"

        # Return the modified response
        return Response(original_data)


# Item Tab 3: Item Vendor
class ItemVendorViewSet(GenericModelViewSet):
    queryset = ItemVendor.objects.all()
    serializer_class = ItemVendorSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item Vendor"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        if "POST" in original_data:
            original_data["POST"]["vendors"]["type"] = "vendor_input"

        if "POST" in original_data:
            original_data["POST"]["vendors"]["column_classes"] = "col-span_3"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "tab-coming-soon"

        # Return the modified response
        return Response(original_data)


# Item Tab 3: Item MSA
class MSAInformationViewSet(GenericModelViewSet):
    queryset = MSAInformation.objects.all()
    serializer_class = MSAInformationSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        if "meta" in original_data:
            original_data["meta"]["title"] = "Item MSA Information"

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = item_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "item"

        if "POST" in original_data:
            original_data["POST"]["item"]["type"] = "hidden"

        if "POST" in original_data:
            original_data["POST"]["promotion_indicator"]["type"] = "radioButton"
        if "POST" in original_data:
            original_data["POST"]["identification_symbol"]["dependency"] = {
                "value": True,
                "name:": "include_in_msa",
            }

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


class PricingAndTaxViewSet(GenericModelViewSet):
    queryset = PricingAndTax.objects.all()
    serializer_class = PricingAndTaxSerializer
    permission_classes = [AllowAny]


# Customer Tab 2: Account Information
class PricingAndTaxCreateViewSet(GenericModelViewSet):
    queryset = PricingAndTax.objects.all()
    serializer_class = PricingAndTaxSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = customer_tab
        if "form" in original_data:
            original_data["form"]["dependency"] = "customer"
        if "POST" in original_data:
            original_data["POST"]["customer"]["type"] = "hidden"
        if "POST" in original_data:
            original_data["POST"]["pricing_model_name"]["type"] = "create_and_select"
        if "POST" in original_data:
            original_data["POST"]["tax_appeal"]["type"] = "radioButton"
        if "POST" in original_data:
            original_data["POST"]["pricing_model_name"]["bindLabel"] = "display_name"
        if "POST" in original_data:
            original_data["POST"]["pricing_model_name"]["bindValue"] = "value"
        if "POST" in original_data:
            original_data["POST"]["pricing_model_name"]["schema"] = {
                "endpoint": "/api/pricing-model/",
                "label": "Create pricing model",
            }
        if "POST" in original_data:
            original_data["POST"]["pricing_model_name"][
                "placeholder"
            ] = "Select pricing model name"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


class ShippingBillingAddressViewSet(GenericModelViewSet):
    queryset = ShippingBillingAddress.objects.all()
    serializer_class = ShippingBillingAddressSerializer
    permission_classes = [AllowAny]


# Customer Tab 3: Shipping & Billing Address
class ShippingBillingAddressCreateViewSet(GenericModelViewSet):
    queryset = ShippingBillingAddress.objects.all()
    serializer_class = ShippingBillingAddressSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key
        new_object = customer_tab

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = new_object
        if "form" in original_data:
            original_data["form"]["dependency"] = "customer"

        if "POST" in original_data:
            original_data["POST"]["customer"]["type"] = "hidden"

        if "POST" in original_data:
            original_data["POST"]["street_address"]["type"] = "google_address"

        if "POST" in original_data:
            original_data["POST"]["street_address"]["schema"] = {
                "isStandalone": False,
                "autoPopulate": {
                    "state": "state",
                    "city": "city",
                    "city": "city",
                    "zip_code": "zip_code",
                },
            }

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class SecInformationViewSet(GenericModelViewSet):
    queryset = SecInformation.objects.all()
    serializer_class = SecInformationSerializer
    permission_classes = [AllowAny]


# Customer Tab 4: Customer Sec Information
class SecInformationCreateViewSet(GenericModelViewSet):
    queryset = SecInformation.objects.all()
    serializer_class = SecInformationSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Add a new object to the 'form' key
        new_object = customer_tab

        # Ensure 'form' exists and update it with the new object
        if "form" in original_data:
            original_data["form"]["tab"] = new_object
        if "form" in original_data:
            original_data["form"]["dependency"] = "customer"
        if "POST" in original_data:
            original_data["POST"]["customer"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "create-edit-only"

        # Return the modified response
        return Response(original_data)


class DashboardView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Dashboard V2"

        return Response(original_data)


class AddressView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "AddressView"

        return Response(original_data)


class PurchaseView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Purchase"

        return Response(original_data)


class SalesInvoiceView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Sales Invoice"

        return Response(original_data)


class AccountView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Account"

        return Response(original_data)


class MasterView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Master"

        return Response(original_data)


class SpecialPricingView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Special Pricing"

        return Response(original_data)


class ProductCatalogView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Product Catalog"

        return Response(original_data)


class SmartOrderingView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Smart Ordering"

        return Response(original_data)


class DispatchView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Dispatch"

        return Response(original_data)


class MessageView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Message"

        return Response(original_data)


class ReportsView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Reports"

        return Response(original_data)


class SettingsView(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Setting"

        return Response(original_data)


class PurchaseOrderViewSet(GenericModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [AllowAny]


class DepartmentViewSet(GenericModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [AllowAny]


class ItemViewSet(GenericModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class ItemManagementViewSet(GenericModelViewSet):
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        original_data = options  # Get the original data

        # Add a new object to the 'form' key
        if "meta" in original_data:
            original_data["meta"]["title"] = "Sales Invoice"

        return Response(original_data)


class PurchaseOrderItemViewSet(GenericModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer
    permission_classes = [AllowAny]


class GoodsInwardViewSet(GenericModelViewSet):
    queryset = GoodsInward.objects.all()
    serializer_class = GoodsInwardSerializer
    permission_classes = [AllowAny]


class GoodsInwardItemViewSet(GenericModelViewSet):
    queryset = GoodsInwardItem.objects.all()
    serializer_class = GoodsInwardItemSerializer
    permission_classes = [AllowAny]


class InventoryViewSet(GenericModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [AllowAny]


class InventoryItemViewSet(GenericModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [AllowAny]


class GoodsReceiptViewSet(GenericModelViewSet):
    """
    ViewSet for managing GoodsReceipt records.
    """

    queryset = GoodsReceipt.objects.all()
    serializer_class = GoodsReceiptSerializer
    permission_classes = [AllowAny]


class GoodsReceiptItemViewSet(GenericModelViewSet):
    """
    ViewSet for managing GoodsReceiptItem records.
    """

    queryset = GoodsReceiptItem.objects.all()
    serializer_class = GoodsReceiptItemSerializer
    permission_classes = [AllowAny]


class EmployeeViewSet(GenericModelViewSet):
    """
    ViewSet for managing Employee records.
    """

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]


class ExpenseViewSet(GenericModelViewSet):
    """
    ViewSet for managing Expense records.
    """

    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]


class CustomerInformationViewSet(GenericModelViewSet):
    """
    ViewSet for managing CustomerInformation records.
    """

    queryset = CustomerInformation.objects.all()
    serializer_class = CustomerInformationSerializer
    permission_classes = [AllowAny]


class SalesOrderViewSet(GenericModelViewSet):
    """
    ViewSet for managing SalesOrder records.
    """

    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [AllowAny]


class ItemInformationModelViewSet(GenericModelViewSet):
    """
    ViewSet for managing ItemInformationModel records.
    """

    queryset = ItemInformation.objects.all()
    serializer_class = ItemInformationModelSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object

        if "meta" in original_data:
            original_data["meta"]["title"] = "Search Items"

        if "form" in original_data:
            original_data["form"]["button"] = {
                "label": "Add Item",
                "link": "/dashboard/add-items",
            }

        if "form" in original_data:
            original_data["form"]["other_config"] = {
                "item_code": {
                    "required": False,
                },
                "item_name": {
                    "required": False,
                },
                "units_of_measurement": {
                    "required": False,
                },
                "department": {
                    "hidden": True,
                },
                "company": {
                    "hidden": True,
                },
                "units_of_measurement": {
                    "hidden": True,
                },
                "weight": {"hidden": True},
                "item_dimension": {"hidden": True},
                "quantity_on_hand": {"hidden": True},
                "qty_per_unit": {"hidden": True},
                "qty_per_unit": {"hidden": True},
                "manufacturer_item_no": {"hidden": True},
                "volume": {"hidden": True},
                "is_active": {"hidden": True},
                "items_to_be_sold_by_units": {"hidden": True},
                "primary_item_category": {
                    "required": False,
                },
                "vendor": {"hidden": True},
                "company_name": {"hidden": True},
            }

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "view-only"

        # Return the modified response
        return Response(original_data)


class SystemViewSet(GenericModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "System"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class OrderHistoryViewSet(GenericModelViewSet):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
    permission_classes = [AllowAny]


class CustomerDetailsViewSet(GenericModelViewSet):
    queryset = CustomerDetails.objects.all()
    serializer_class = CustomerDetailsSerializer
    permission_classes = [AllowAny]  # Allow unrestricted access


# ViewSet for ItemCategory
class ItemCategoryViewSet(GenericModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Category"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


class ItemSecondaryCategoryViewSet(GenericModelViewSet):
    queryset = ItemSecondaryCategory.objects.all()
    serializer_class = ItemSecondaryCategorySerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "Secondary Category"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "on-page-edit"

        # Return the modified response
        return Response(original_data)


# ViewSet for ItemDetails
class ItemDetailsViewSet(GenericModelViewSet):
    queryset = ItemDetails.objects.all()
    serializer_class = ItemDetailsSerializer
    permission_classes = [AllowAny]


# ViewSet for Invoice
class InvoiceViewSet(GenericModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object
        if "meta" in original_data:
            original_data["meta"]["title"] = "System"
        if "layout" in original_data:
            original_data["layout"][0]["template"] = "invoice-template"

        # Return the modified response
        return Response(original_data)


class InvoiceListViewSet(GenericModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [AllowAny]

    def options(self, request, *args, **kwargs):
        # Call the parent class's `options` method to get the default metadata
        response = super().options(request, *args, **kwargs)
        original_data = response.data  # Get the original data

        # Ensure 'form' exists and update it with the new object

        if "meta" in original_data:
            original_data["meta"]["title"] = "Invoice List"

        if "form" in original_data:
            original_data["form"]["button"] = {
                "label": "Add Item",
                "link": "/dashboard/invoices",
            }

        fields_to_hide = [
            "cash_and_carry",
            "delivery_date",
            "po",
            "is_cash_and_carry_customer_code",
            "shipping_delivery_type",
            "cash_and_carry_customer_code",
            "billing_address",
            "cigarette_license",
            "delivery_type",
            "customer_notes",
            "total_quantity",
            "total_amount",
            "total_discount",
            "total_excise_tax",
            "customer",
            "customer_type",
            "invoiceList",
            "salesman",
            "customer_info.id",
            "customer_info.customer_code",
            "customer_info.customer_name",
            "customer_info.contact_person_name",
            "customer_info.phone",
            "customer_info.email",
            "customer_info.fax",
            "customer_info.boro",
            "customer_info.credit_limit",
            "customer_info.product_promotion",
            "customer_info.customer_note",
            "customer_info.is_active",
            "customer_info.is_msa_include",
            "customer_info.is_sales_tax_applicable",
            "customer_info.send_email_on_invoice_creation",
            "customer_info.calculate_interest",
            "customer_info.self_checkout_tax",
            "customer_info.cash_and_carry_customer_code",
            "customer_info.salesman",
            "customer_info.customer_type",
            "customer_info.payment_terms",
            "customer_info.customer_group",
            "customer_info.company",
        ]
        if "POST" in original_data:
            for field in fields_to_hide:
                if field in original_data["POST"]:
                    original_data["POST"][field]["type"] = "hidden"

        # if "POST" in original_data:
        #     original_data["POST"]["cash_and_carry"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["delivery_date"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["po"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["is_cash_and_carry_customer_code"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["shipping_delivery_type"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["cash_and_carry_customer_code"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["billing_address"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["cigarette_license"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["delivery_type"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["customer_notes"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["total_quantity"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["total_amount"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["total_discount"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["total_excise_tax"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["customer"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["customer_type"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["invoiceList"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["salesman"]["type"] = "hidden"
        # if "POST" in original_data:
        #     original_data["POST"]["customer_code"]["type"] = "hidden"

        if "layout" in original_data:
            original_data["layout"][0]["template"] = "view-only"

        # Return the modified response
        return Response(original_data)


class InvoiceItemViewSet(GenericModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceItemSerializer
    permission_classes = [AllowAny]


class InvoiceTypeViewSet(
    GenericModelViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
):
    """
    ViewSet for InvoiceType.
    """

    queryset = InvoiceType.objects.all()
    serializer_class = InvoiceTypeSerializer
    permission_classes = [AllowAny]


class InvoiceHistoryViewSet(
    GenericModelViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
):
    """
    ViewSet for InvoiceHistory.
    """

    queryset = InvoiceHistory.objects.all().select_related(
        "customer", "invoice_type"
    )  # Use select_related for performance optimization
    serializer_class = InvoiceHistorySerializer
    permission_classes = [AllowAny]
