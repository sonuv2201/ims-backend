from django.urls import path, include  # Import `path` and `include`
from rest_framework.routers import DefaultRouter
from ims.views import (
    CustomerViewSet,
    SalesmanViewSet,
    CompanyNameViewSet,
    CustomerTypeViewSet,
    PaymentTermsViewSet,
    CustomerGroupViewSet,
    ProductionPromotionViewSet,
    PricingModelViewSet,
    PricingAndTaxViewSet,
    ShippingBillingAddressViewSet,
    SecInformationViewSet,
    DashboardView,
    PurchaseView,
    SalesInvoiceView,
    AccountView,
    MasterView,
    SpecialPricingView,
    ProductCatalogView,
    SmartOrderingView,
    DispatchView,
    MessageView,
    ReportsView,
    SettingsView,
    CreateCustomerViewSet,
    SecInformationCreateViewSet,
    ShippingBillingAddressCreateViewSet,
    PricingAndTaxCreateViewSet,
    VendorViewSet,
    ItemViewSet,
    PurchaseOrderViewSet,
    PurchaseOrderItemViewSet,
    GoodsInwardViewSet,
    GoodsInwardItemViewSet,
    InventoryViewSet,
    InventoryItemViewSet,
    GoodsReceiptViewSet,
    GoodsReceiptItemViewSet,
    EmployeeViewSet,
    ExpenseViewSet,
    CustomerInformationViewSet,
    SalesOrderViewSet,
    ItemInformationModelViewSet,
    SystemViewSet,
    OrderHistoryViewSet,
    CustomerDetailsViewSet,
    ItemCategoryViewSet,
    ItemSecondaryCategoryViewSet,
    ItemDetailsViewSet,
    InvoiceViewSet,
    InvoiceItemViewSet,
    InvoiceTypeViewSet,
    InvoiceHistoryViewSet,
    SearchCustomerViewSet,
    AddItemViewSet,
    BrandViewSet,
    ItemManagementViewSet,
    UpCViewSet,
    SecItemInformationViewSet,
    ItemTaxViewSet,
    ItemCashViewSet,
    MSAInformationViewSet,
    VendorSecViewSet,
    CreateVendorViewSet,
    VendorShippingBillingAddressViewSet,
    # CityViewSet,
    StateViewSet,
    # ZipCodeViewSet,
    # CountryViewSet,
    TaxViewSet,
    VendorViewSet,
    SearchVendorViewSet,
    AddressView,
    ItemPriceViewSet,
    ItemVendorViewSet,
    SearchTaxViewSet,
    DepartmentViewSet,
    CustomerSpecialPricingView,
    SpecialItemPriceViewSet,
    SpecialPricingClassificationViewSet,
    SpecialPricingClassificationListingViewSet,
    InvoiceListViewSet,
)

# Define the router and register viewsets
router = DefaultRouter()

router.register(r"invoice-list", InvoiceListViewSet, basename="invoice-list")
router.register(r"address", AddressView, basename="address")
router.register(r"tax", TaxViewSet, basename="tax")
# router.register(r"city", CityViewSet, basename="city")
router.register(r"state", StateViewSet, basename="state")
# router.register(r"zip-code", ZipCodeViewSet, basename="zip-code")
# router.register(r"country", CountryViewSet, basename="country")

router.register(r"settings", SettingsView, basename="settings")
router.register(r"reports", ReportsView, basename="reports")
router.register(r"message", MessageView, basename="message")
router.register(r"dispatch", DispatchView, basename="dispatch")
router.register(r"smart-ordering", SmartOrderingView, basename="smart_ordering")
router.register(r"product-catalog", ProductCatalogView, basename="product_catalog")
router.register(r"special-pricing", SpecialPricingView, basename="special_pricing")
router.register(r"master", MasterView, basename="master")
router.register(r"account", AccountView, basename="account")
router.register(r"sales-invoice", SalesInvoiceView, basename="sales_invoice")
router.register(r"purchase", PurchaseView, basename="purchase")
router.register(r"dashboard-view", DashboardView, basename="dashboard_view")
router.register(
    r"create-sec-information",
    SecInformationCreateViewSet,
    basename="create_sec_information",
)
router.register(r"sec-information", SecInformationViewSet, basename="sec_information")
router.register(
    r"create-shipping-billing-address",
    ShippingBillingAddressCreateViewSet,
    basename="create-shipping_billing_address",
)
router.register(
    r"shipping-billing-address",
    ShippingBillingAddressViewSet,
    basename="shipping_billing_address",
)
router.register(
    r"create-pricing-and-tax",
    PricingAndTaxCreateViewSet,
    basename="create-pricing_and_tax",
)
router.register(r"search-tax", SearchTaxViewSet, basename="search-tax")
router.register(r"pricing-and-tax", PricingAndTaxViewSet, basename="pricing_and_tax")
router.register(r"pricing-model", PricingModelViewSet, basename="pricing_model")
router.register(r"customer", CustomerViewSet, basename="customer")
router.register(r"search-customer", SearchCustomerViewSet, basename="search-customer")
router.register(r"create-customer", CreateCustomerViewSet, basename="create-customer")
router.register(r"salesman", SalesmanViewSet, basename="salesman")
router.register(
    r"customer-company-name", CompanyNameViewSet, basename="customer_company_name"
)
router.register(r"customer-type", CustomerTypeViewSet, basename="customer_type")
router.register(r"payment-terms", PaymentTermsViewSet, basename="payment_terms")
router.register(r"customer-group", CustomerGroupViewSet, basename="customer_group")
router.register(
    r"production-promotion", ProductionPromotionViewSet, basename="production_promotion"
)
router.register(r"vendor", VendorViewSet, basename="vendor")
router.register(r"search-vendor", SearchVendorViewSet, basename="search-vendor")

router.register(
    r"create-vendor",
    CreateVendorViewSet,
    basename="create-vendor",
)
router.register(
    r"vendor-sec-information",
    VendorSecViewSet,
    basename="vendor-sec-information",
)
router.register(
    r"vendor-shipping-billing-address",
    VendorShippingBillingAddressViewSet,
    basename="vendor-shipping-billing-address",
)

router.register(r"item", ItemViewSet, basename="item")
router.register(r"purchase-order", PurchaseOrderViewSet, basename="purchase_order")
router.register(
    r"purchase-order-item", PurchaseOrderItemViewSet, basename="purchase_order_item"
)
router.register(r"goods-inward", GoodsInwardViewSet, basename="goods_inward")
router.register(
    r"goods-inward-item", GoodsInwardItemViewSet, basename="goods_inward_item"
)
router.register(r"inventories", InventoryViewSet, basename="inventory")
router.register(r"inventory-items", InventoryItemViewSet, basename="inventory-item")
router.register(r"goods-receipts", GoodsReceiptViewSet, basename="goods-receipt")
router.register(
    r"goods-receipt-items", GoodsReceiptItemViewSet, basename="goods-receipt-item"
)
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(
    r"customers-information",
    CustomerInformationViewSet,
    basename="customer-information",
)
router.register(r"sales-orders", SalesOrderViewSet, basename="sales-order")
router.register(
    r"items-information", ItemInformationModelViewSet, basename="item-information-model"
)
router.register(r"add-items", AddItemViewSet, basename="add-item-view-set")
router.register(r"order-history", OrderHistoryViewSet, basename="order-history")
router.register(r"system", SystemViewSet, basename="system")
router.register(
    r"customers-details", CustomerDetailsViewSet, basename="customers-details"
)
router.register(r"itemcategories", ItemCategoryViewSet, basename="item-categories")
router.register(
    r"item-secondary-categories",
    ItemSecondaryCategoryViewSet,
    basename="item-secondary-categories",
)
router.register(r"create-brand", BrandViewSet, basename="create-brand")
router.register(r"item-management", ItemManagementViewSet, basename="item-management")
router.register(r"items-details", ItemDetailsViewSet, basename="items-details")
router.register(r"invoices", InvoiceViewSet, basename="invoices")
router.register(r"invoice-items", InvoiceItemViewSet, basename="invoice_items")
router.register(r"invoice-types", InvoiceTypeViewSet, basename="invoice_types")
router.register(r"invoice-history", InvoiceHistoryViewSet, basename="invoice_history")
router.register(r"item-upc", UpCViewSet, basename="item-upc")
router.register(
    r"item-sec-information", SecItemInformationViewSet, basename="item-sec-information"
)
router.register(r"item-tax", ItemTaxViewSet, basename="item-tax")
router.register(r"item-cash", ItemCashViewSet, basename="item-cash")
router.register(r"item-price", ItemPriceViewSet, basename="item-price")
router.register(r"department", DepartmentViewSet, basename="department")
router.register(r"item-vendor", ItemVendorViewSet, basename="item-vendor")
router.register(
    r"item-msa-information", MSAInformationViewSet, basename="item-msa-information"
)
router.register(
    r"customer-special-pricing-item",
    CustomerSpecialPricingView,
    basename="customer-special-pricing-item",
)
router.register(
    r"customer-special-pricing",
    SpecialPricingClassificationViewSet,
    basename="customer-special-pricing",
)
router.register(
    r"customer-special-pricing-list",
    SpecialPricingClassificationListingViewSet,
    basename="customer-special-pricing-list",
)
router.register(
    r"special-item-price",
    SpecialItemPriceViewSet,
    basename="special-item-price",
)


urlpatterns = router.urls
