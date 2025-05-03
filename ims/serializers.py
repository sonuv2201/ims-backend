from rest_framework import serializers
from datetime import datetime

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
    State,
    # City,
    # ZipCode,
    Tax,
    Department,
    ItemPrice,
    ItemVendor,
    CustomerSpecialPricing,
    SpecialPricingClassification,
    ItemSecondaryCategory,
)


class SpecialPricingClassificationSerializer(serializers.ModelSerializer):
    expire = serializers.SerializerMethodField()

    class Meta:
        model = SpecialPricingClassification
        fields = "__all__"

    def get_expire(self, obj):
        """Check if expiry_date has passed."""
        if obj.expiry_date:
            # Convert expiry_date string to a datetime object
            expiry_date = datetime.strptime(obj.expiry_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            # Check if the expiry date has passed
            if expiry_date < datetime.utcnow():
                return True
        return False


class CustomerSpecialPricingSerializer(serializers.ModelSerializer):
    # price_classification = SpecialPricingClassificationSerializer()
    price_classification = serializers.PrimaryKeyRelatedField(
        queryset=SpecialPricingClassification.objects.all()
    )
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), required=False, allow_null=True
    )
    customer_group = serializers.PrimaryKeyRelatedField(
        queryset=CustomerGroup.objects.all(), required=False, allow_null=True
    )
    item = serializers.PrimaryKeyRelatedField(
        queryset=ItemInformation.objects.all(), required=False, allow_null=True
    )
    primary_category = serializers.PrimaryKeyRelatedField(
        queryset=ItemCategory.objects.all(), required=False, allow_null=True
    )
    secondary_category = serializers.PrimaryKeyRelatedField(
        queryset=ItemSecondaryCategory.objects.all(), required=False, allow_null=True
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = CustomerSpecialPricing
        fields = "__all__"


class ItemVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVendor
        fields = "__all__"


class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = "__all__"


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = "__all__"


class ItemSecondaryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSecondaryCategory
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class SecItemSerializer(serializers.ModelSerializer):

    secondary_item_category_info = ItemSecondaryCategorySerializer(
        source="secondary_item_category", read_only=True
    )

    class Meta:
        model = SecItemInformation
        fields = [
            "id",
            "secondary_item_no",
            "expire_date",
            "locations",
            "size",
            "secondary_item_category",
            "secondary_item_category_info",
            "brand",
            "item",
            "system",
        ]


class SpecialItemPriceSerializer(serializers.ModelSerializer):
    item_price = serializers.SerializerMethodField()
    primary_item_category = ItemCategorySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    sec_information = serializers.SerializerMethodField()

    class Meta:
        model = ItemInformation
        fields = "__all__"

    def get_item_price(self, obj):
        item_price = ItemPrice.objects.filter(item=obj).first()
        if item_price:
            return ItemPriceSerializer(item_price).data
        return None

    def get_sec_information(self, obj):
        sec_information = SecItemInformation.objects.filter(item=obj).first()
        if sec_information:
            return SecItemSerializer(
                sec_information
            ).data  # Will return full nested data for sec_information
        return None


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"


# class ZipCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ZipCode
#         fields = "__all__"


# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = "__all__"


# class CitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = City
#         fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class VendorSecondaryInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorSecondaryInformation
        fields = "__all__"


class VendorShippingBillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorShippingBillingAddress
        fields = "__all__"


class ItemCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCash
        fields = "__all__"


class MSAInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MSAInformation
        fields = "__all__"


class UPCModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UPC
        fields = "__all__"


class ItemTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTax
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class PricingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingModel
        fields = "__all__"


class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = "__all__"


class PaymentTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerms
        fields = "__all__"


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = "__all__"


class ProductionPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionPromotion
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class PricingAndTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingAndTax
        fields = "__all__"


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class ShippingBillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingBillingAddress
        fields = "__all__"


class SecInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecInformation
        fields = "__all__"


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    purchase_order = PurchaseOrderSerializer(read_only=True)
    item = ItemSerializer(read_only=True)

    class Meta:
        model = PurchaseOrderItem
        fields = "__all__"


class GoodsInwardItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsInwardItem
        fields = "__all__"


class GoodsInwardSerializer(serializers.ModelSerializer):
    items = GoodsInwardItemSerializer(many=True, read_only=True)

    class Meta:
        model = GoodsInward
        fields = "__all__"


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(
        many=True, read_only=True
    )  # Nested serializer for related items

    class Meta:
        model = Inventory
        fields = "__all__"


class GoodsReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsReceiptItem
        fields = "__all__"


class GoodsReceiptSerializer(serializers.ModelSerializer):
    items = GoodsReceiptItemSerializer(
        many=True, read_only=True
    )  # Nested serializer for related items

    class Meta:
        model = GoodsReceipt
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(
        read_only=True
    )  # Nested serializer to display employee details

    class Meta:
        model = Expense
        fields = "__all__"


class CustomerInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInformation
        fields = "__all__"


class ItemInformationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInformation
        fields = "__all__"


class SalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesman
        fields = "__all__"


class SalesOrderSerializer(serializers.ModelSerializer):
    # Nested serializer to include customer and items details
    customer = CustomerInformationSerializer(
        read_only=True
    )  # Read-only nested customer details
    items = ItemInformationModelSerializer(
        many=True, read_only=True
    )  # Read-only nested items details

    class Meta:
        model = SalesOrder
        fields = "__all__"


class SystemSerializer(serializers.ModelSerializer):
    """
    Serializer for the System model.
    """

    class Meta:
        model = System
        fields = ["id", "name"]  # Include all fields that should be exposed in the API.


class OrderHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderHistory model.
    """

    customer_name = serializers.CharField(
        source="customer.name", read_only=True
    )  # Display the customer's name.
    system_name = serializers.CharField(
        source="system.name", read_only=True
    )  # Display the system's name.

    class Meta:
        model = OrderHistory
        fields = [
            "id",
            "order_number",
            "customer",  # Foreign key reference.
            "customer_name",  # Human-readable customer name.
            "system",  # Foreign key reference.
            "system_name",  # Human-readable system name.
            "status",
            "section",
            "total_amount",
            "created_date",
            "updated_date",
        ]
        read_only_fields = [
            "created_date",
            "updated_date",
        ]  # Prevent modification of auto-generated fields.


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = "__all__"  # Include all fields in the serialized output


class ItemDetailsSerializer(serializers.ModelSerializer):
    category = ItemCategorySerializer(
        read_only=True
    )  # Nested serializer to include category details

    class Meta:
        model = ItemDetails
        fields = "__all__"


class InvoiceItemSerializer(serializers.ModelSerializer):
    item = ItemDetailsSerializer(
        read_only=True
    )  # Nested serializer to include item details

    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    customer_info = CustomerSerializer(source="customer", read_only=True)

    class Meta:
        model = Invoice
        fields = "__all__"


class InvoiceTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for InvoiceType model.
    """

    class Meta:
        model = InvoiceType
        fields = "__all__"


class InvoiceHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for InvoiceHistory model.
    """

    customer_name = serializers.CharField(
        source="customer.name", read_only=True
    )  # Include customer's name as a read-only field
    invoice_type_name = serializers.CharField(
        source="invoice_type.name", read_only=True
    )  # Include invoice type name as a read-only field

    class Meta:
        model = InvoiceHistory
        fields = [
            "id",
            "customer",
            "customer_name",
            "invoice_no",
            "created_date",
            "status",
            "invoice_type",
            "invoice_type_name",
            "quantity",
            "total_amount",
        ]
