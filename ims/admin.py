from django.contrib import admin
from ims.models import (
    Customer,
    Salesman,
    CustomerType,
    Company,
    PaymentTerms,
    CustomerGroup,
    ProductionPromotion,
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
    OrderHistory,
    CustomerDetails,
    ItemCategory,
    ItemDetails,
    Invoice,
    InvoiceItem,
    InvoiceType,
    InvoiceHistory,
    PricingModel,
    Department,
    Brand,
    PricingAndTax,
    SecInformation,
    CustomerSpecialPricing,
    State,
    SpecialPricingClassification,
    ItemSecondaryCategory,
    ItemPrice,
)

from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Customizing the Admin Site
admin.site.site_header = "ims Administration"
admin.site.site_title = "ims Admin Portal"
admin.site.index_title = "Welcome to ims Admin Panel"


# Define resources for each model
class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


class SalesmanResource(resources.ModelResource):
    class Meta:
        model = Salesman


class CustomerTypeResource(resources.ModelResource):
    class Meta:
        model = CustomerType


class CompanyNameResource(resources.ModelResource):
    class Meta:
        model = Company


class PaymentTermsResource(resources.ModelResource):
    class Meta:
        model = PaymentTerms


class CustomerGroupResource(resources.ModelResource):
    class Meta:
        model = CustomerGroup


class ProductionPromotionResource(resources.ModelResource):
    class Meta:
        model = ProductionPromotion


class VendorResource(resources.ModelResource):
    class Meta:
        model = Vendor


class PurchaseOrderResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrder


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item


class PurchaseOrderItemResource(resources.ModelResource):
    class Meta:
        model = PurchaseOrderItem


class GoodsInwardResource(resources.ModelResource):
    class Meta:
        model = GoodsInward


class GoodsInwardItemResource(resources.ModelResource):
    class Meta:
        model = GoodsInwardItem


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee


class ExpenseResource(resources.ModelResource):
    class Meta:
        model = Expense


class CustomerInformationResource(resources.ModelResource):
    class Meta:
        model = Expense


class SalesOrderResource(resources.ModelResource):
    class Meta:
        model = SalesOrder


class ItemInformationResource(resources.ModelResource):
    class Meta:
        model = ItemInformation


class SystemResource(resources.ModelResource):
    class Meta:
        model = System


class OrderHistoryResource(resources.ModelResource):
    class Meta:
        model = OrderHistory


class CustomerDetailsResource(resources.ModelResource):
    class Meta:
        model = CustomerDetails


class ItemCategoryResource(resources.ModelResource):
    class Meta:
        model = ItemCategory


class ItemDetailsResource(resources.ModelResource):
    class Meta:
        model = ItemDetails


class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice


class InvoiceItemResource(resources.ModelResource):
    class Meta:
        model = InvoiceItem


class InvoiceHistoryResource(resources.ModelResource):
    class Meta:
        model = InvoiceHistory


# Resource for InvoiceType
class InvoiceTypeResource(resources.ModelResource):
    class Meta:
        model = InvoiceType


# Registering models with import-export functionality
@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    pass


@admin.register(Salesman)
class SalesmanAdmin(ImportExportModelAdmin):
    resource_class = SalesmanResource
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(CustomerType)
class CustomerTypeAdmin(ImportExportModelAdmin):
    resource_class = CustomerTypeResource
    list_display = ("id", "customer_type")
    search_fields = ("customer_type",)


@admin.register(Company)
class CompanyNameAdmin(ImportExportModelAdmin):
    resource_class = CompanyNameResource
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(PaymentTerms)
class PaymentTermsAdmin(ImportExportModelAdmin):
    resource_class = PaymentTermsResource
    list_display = ("id", "term_name")
    search_fields = ("term_name",)


@admin.register(CustomerGroup)
class CustomerGroupAdmin(ImportExportModelAdmin):
    resource_class = CustomerGroupResource


@admin.register(ProductionPromotion)
class ProductionPromotionAdmin(ImportExportModelAdmin):
    resource_class = ProductionPromotionResource
    list_display = ("id", "group_name")
    search_fields = ("group_name",)


@admin.register(Vendor)
class VendorAdmin(ImportExportModelAdmin):
    resource_class = VendorResource
    list_display = (
        "id",
        "vendor_name",
        "vendor_id",
    )  # Updated fields based on the model
    search_fields = ("vendor_name",)  # Adjusted search fields to match the model fields
    list_filter = ()  # Removed 'is_active' as it does not exist in the model


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_class = ItemResource
    list_display = ("id", "upc_code", "name", "cost_price", "selling_price", "volume")
    search_fields = ("upc_code", "name")  # Matches fields from the Item model


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(ImportExportModelAdmin):
    resource_class = PurchaseOrderResource
    list_display = (
        # 'id',
        "vendor_po_number",
        "vendor",
        "purchase_order_date",
        "expected_delivery_date",
        "delivery_status",
    )  # Updated fields to match the PurchaseOrder model
    search_fields = ("vendor_po_number", "vendor__name", "delivery_status")
    list_filter = ("delivery_status", "purchase_order_date")
    exclude = ["id"]


@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(ImportExportModelAdmin):
    resource_class = PurchaseOrderItemResource
    # list_display = ('id', 'purchase_order', 'item', 'quantity', 'total_cost')
    list_display = ("purchase_order", "item", "quantity", "total_cost")
    search_fields = ("purchase_order__vendor_po_number", "item__name")
    exclude = ["id"]


@admin.register(GoodsInward)
class GoodsInwardAdmin(ImportExportModelAdmin):
    resource_class = GoodsInwardResource
    list_display = (
        "id",
        "goods_inward_no",
        "vendor_name",
        "purchase_order_no",
        "inward_date",
        "status",
    )  # Use 'purchase_order_no'
    search_fields = (
        "goods_inward_no",
        "vendor_name",
        "purchase_order__id",
    )  # Use '__' for foreign key reference
    list_filter = ("status", "inward_date")
    ordering = ("-inward_date",)


@admin.register(GoodsInwardItem)
class GoodsInwardItemAdmin(ImportExportModelAdmin):
    list_display = ("goods_inward", "item_code", "po_qty", "rec_qty", "case_qty")
    search_fields = ("item_code", "goods_inward__goods_inward_no")
    list_filter = ("goods_inward__inward_date",)


@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin):
    list_display = (
        "purchase_invoice_number",
        "purchase_date",
        "section",
        "is_price_updated",
        "created_by",
        "updated_by",
    )
    search_fields = ("purchase_invoice_number", "section")
    list_filter = ("purchase_date", "is_price_updated")


@admin.register(InventoryItem)
class InventoryItemAdmin(ImportExportModelAdmin):
    list_display = (
        "inventory",
        "item_number",
        "item_name",
        "quantity",
        "selling_price",
    )
    search_fields = ("item_number", "item_name", "inventory__purchase_invoice_number")
    list_filter = ("inventory__purchase_date",)


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(ImportExportModelAdmin):
    list_display = ("goods_receipt_date", "invoice_number", "section")
    search_fields = ("invoice_number", "section")
    list_filter = ("goods_receipt_date",)


@admin.register(GoodsReceiptItem)
class GoodsReceiptItemAdmin(ImportExportModelAdmin):
    list_display = (
        "goods_receipt",
        "item_number",
        "item_name",
        "quantity_in_stock",
        "quantity_ordered",
        "price",
    )
    search_fields = ("item_number", "item_name", "goods_receipt__invoice_number")
    list_filter = ("goods_receipt__goods_receipt_date",)


@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")  # Display ID and name in the admin list view
    search_fields = ("name",)  # Add search functionality for name


@admin.register(Expense)
class ExpenseAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "expense_name",
        "employee",
        "amount",
        "expense_date",
        "payment_mode",
        "created_date",
    )
    list_filter = (
        "payment_mode",
        "expense_date",
        "created_date",
    )  # Add filters for payment mode and dates
    search_fields = (
        "expense_name",
        "employee__name",
    )  # Add search functionality for expense name and employee name
    date_hierarchy = "expense_date"  # Enable date navigation for expense_date


@admin.register(CustomerInformation)
class CustomerInformationAdmin(ImportExportModelAdmin):
    """
    Admin configuration for CustomerInformation.
    """

    list_display = (
        "id",
        "name",
        "customer_type",
        "outstanding_balance",
        "last_payment_date",
    )
    list_filter = (
        "customer_type",
        "last_payment_date",
    )  # Filters for customer type and payment date
    search_fields = (
        "name",
        "shipping_address",
        "billing_address",
    )  # Search by name, shipping, and billing address
    ordering = ("name",)


@admin.register(SalesOrder)
class SalesOrderAdmin(ImportExportModelAdmin):
    """
    Admin configuration for SalesOrder.
    """

    list_display = (
        "id",
        "order_no",
        "ordered_by",
        "order_date",
        "delivery_date",
        "delivery_type",
        "customer",
    )
    list_filter = (
        "delivery_type",
        "order_date",
        "delivery_date",
    )  # Filters for delivery type and dates
    search_fields = (
        "order_no",
        "ordered_by",
        "customer__name",
    )  # Search by order no, ordered by, and customer name
    date_hierarchy = "order_date"  # Enable date navigation for order_date
    ordering = ("order_date",)


# @admin.register(ItemInformation)
# class ItemInformationAdmin(ImportExportModelAdmin):
#     """
#     Admin configuration for ItemInformation.
#     """
#     list_display = ('id', 'sales_order', 'item_no', 'description', 'quantity_ordered', 'actual_price', 'total_price')
#     list_filter = ('sales_order',)  # Filter by related sales order
#     search_fields = ('item_no', 'description', 'sales_order__order_no')  # Search by item no, description, and sales order
#     ordering = ('sales_order',)


@admin.register(System)
class SystemAdmin(ImportExportModelAdmin):
    """
    Admin configuration for System.
    """

    list_display = ("id", "name")  # Display the id and name of the system
    search_fields = ("name",)  # Search by the name of the system
    ordering = ("name",)  # Order by name


@admin.register(OrderHistory)
class OrderHistoryAdmin(ImportExportModelAdmin):
    """
    Admin configuration for OrderHistory.
    """

    list_display = (
        "order_number",
        "customer",
        "system",
        "status",
        "section",
        "total_amount",
        "created_date",
        "updated_date",
    )  # Display relevant fields
    list_filter = (
        "status",
        "system",
        "created_date",
    )  # Filter by status, system, and created date
    search_fields = (
        "order_number",
        "customer__name",
        "status",
        "system__name",
    )  # Search by order number, customer name, status, and system name
    date_hierarchy = "created_date"  # Enable date navigation for created_date
    ordering = ("created_date",)  # Order by created_date


@admin.register(CustomerDetails)
class CustomerDetailsAdmin(ImportExportModelAdmin):
    """
    Admin configuration for CustomerDetails.
    """

    list_display = (
        "name",
        "last_payment_amount",
        "outstanding_balance",
    )  # Display relevant fields
    search_fields = ("name",)  # Enable search by customer name
    ordering = ("name",)  # Order by name


@admin.register(ItemCategory)
class ItemCategoryAdmin(ImportExportModelAdmin):
    """
    Admin configuration for ItemCategory.
    """

    list_display = ("category_name",)  # Display category name
    search_fields = ("category_name",)  # Enable search by category name
    ordering = ("category_name",)  # Order by name


@admin.register(ItemDetails)
class ItemDetailsAdmin(ImportExportModelAdmin):
    """
    Admin configuration for ItemDetails.
    """

    list_display = (
        "name",
        "upc_code",
        "category",
        "price",
        "excise_tax",
    )  # Display relevant fields
    list_filter = ("category",)  # Filter by category
    search_fields = (
        "name",
        "upc_code",
        "category__name",
    )  # Search by item name, UPC code, and category name
    ordering = ("name",)  # Order by name


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    """
    Admin configuration for Invoice.
    """

    list_display = (
        "invoice_no",
        "customer",
        "invoice_date",
        "total_quantity",
        "total_amount",
        "total_discount",
        "total_excise_tax",
    )  # Display relevant fields
    list_filter = ("invoice_date",)  # Filter by invoice date
    search_fields = (
        "invoice_no",
        "customer__name",
    )  # Search by invoice number and customer name
    date_hierarchy = "invoice_date"  # Enable date navigation for invoice_date
    ordering = ("-invoice_date",)  # Order by most recent invoice


@admin.register(InvoiceItem)
class InvoiceItemAdmin(ImportExportModelAdmin):
    """
    Admin configuration for InvoiceItem.
    """

    list_display = (
        "invoice",
        "item",
        "quantity",
        "price_per_unit",
        "total_price",
        "discount",
    )  # Display relevant fields
    list_filter = ("invoice", "item")  # Filter by invoice and item
    search_fields = (
        "invoice__invoice_no",
        "item__name",
    )  # Search by invoice number and item name
    ordering = ("invoice",)  # Order by invoice


@admin.register(InvoiceType)
class InvoiceTypeAdmin(ImportExportModelAdmin):
    resource_class = InvoiceTypeResource
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(InvoiceHistory)
class InvoiceHistoryAdmin(ImportExportModelAdmin):
    resource_class = InvoiceHistoryResource
    list_display = (
        "id",
        "invoice_no",
        "customer",
        "created_date",
        "status",
        "invoice_type",
        "quantity",
        "total_amount",
    )
    list_filter = ("status", "invoice_type", "created_date")
    search_fields = ("invoice_no", "customer__customer_name")
    date_hierarchy = "created_date"
    ordering = ("-created_date",)


@admin.register(PricingModel)
class PricingModel(ImportExportModelAdmin):
    pass


@admin.register(Department)
class DepartmentModel(ImportExportModelAdmin):
    pass


@admin.register(Brand)
class BrandModel(ImportExportModelAdmin):
    pass


@admin.register(PricingAndTax)
class PricingAndTax(ImportExportModelAdmin):
    pass


@admin.register(SecInformation)
class CustomerSecInformation(ImportExportModelAdmin):
    pass


@admin.register(CustomerSpecialPricing)
class SpecialPricing(ImportExportModelAdmin):
    pass


@admin.register(SpecialPricingClassification)
class SpecialPricingClassification(ImportExportModelAdmin):
    pass


@admin.register(State)
class StateList(ImportExportModelAdmin):
    pass


@admin.register(ItemSecondaryCategory)
class StateList(ImportExportModelAdmin):
    pass


@admin.register(ItemInformation)
class StateList(ImportExportModelAdmin):
    pass


@admin.register(ItemPrice)
class StateList(ImportExportModelAdmin):
    pass
