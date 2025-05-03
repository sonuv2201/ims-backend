from django.db import models, IntegrityError
from django.core.exceptions import ValidationError


# class Country(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.code}"


# class City(models.Model):
#     name = models.CharField(max_length=100)
#     state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

#     def __str__(self):
#         return f"{self.name}, {self.state.name}"


# class ZipCode(models.Model):
#     code = models.CharField(max_length=10, unique=True)
#     city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="zip_codes")

#     def __str__(self):
#         return f"{self.code} - {self.city.name}, {self.city.state.name}"


class Salesman(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomerType(models.Model):
    customer_type = models.CharField(max_length=255)
    cash_and_carry_percentage = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.customer_type


class PaymentTerms(models.Model):
    term_name = models.CharField(max_length=255)

    def __str__(self):
        return self.term_name


class CustomerGroup(models.Model):

    customer_group_code = models.CharField(max_length=255, unique=True)
    customer_group_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)

    def __str__(self):
        return self.customer_group_name


class ProductionPromotion(models.Model):

    group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.group_name


class ItemCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_price = models.CharField(max_length=50)
    category_code = models.CharField(max_length=50)
    category_description = models.CharField(
        max_length=50, blank=True, null=True, default="Unknown"
    )
    category_type = models.CharField(
        max_length=50, blank=True, null=True, default="Unknown"
    )
    category_system = models.CharField(
        max_length=50, blank=True, null=True, default="Unknown"
    )
    is_cigarette_category = models.BooleanField(default=False)
    is_electronics_cigarette = models.BooleanField(default=False)
    # is_secondary = models.BooleanField(default=False)
    is_none_sales_category = models.BooleanField(default=False)
    is_beverage = models.BooleanField(default=False)

    # parent = models.ForeignKey(
    #     "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    # )

    def __str__(self):
        return self.category_name

    # @property
    # def is_leaf(self):
    #     # A leaf node has no children
    #     return not self.children.exists()


class ItemSecondaryCategory(models.Model):
    category_name = models.CharField(max_length=50)
    category_price = models.CharField(max_length=50)
    category_code = models.CharField(max_length=50)
    category_description = models.CharField(
        max_length=50, blank=True, null=True, default="Unknown"
    )
    category_type = models.CharField(
        max_length=50, blank=True, null=True, default="Unknown"
    )
    category_system = models.CharField(
        max_length=50, blank=True, null=True, default="Unknown"
    )
    is_cigarette_category = models.BooleanField(default=False)
    is_electronics_cigarette = models.BooleanField(default=False)
    # is_secondary = models.BooleanField(default=False)
    is_none_sales_category = models.BooleanField(default=False)
    is_beverage = models.BooleanField(default=False)

    # parent = models.ForeignKey(
    #     "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    # )

    def __str__(self):
        return self.category_name

    # @property
    # def is_leaf(self):
    #     # A leaf node has no children
    #     return not self.children.exists()


class PricingModel(models.Model):
    pricing_model_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # item_category = models.CharField(max_length=255)
    item_category = models.ForeignKey(
        ItemCategory, related_name="pricing_item_category", on_delete=models.CASCADE
    )

    pricing_model_amount = models.CharField(max_length=255)
    pricing_model_amount_type = models.CharField(
        max_length=100,
        choices=[("fixed", "Fixed"), ("percentage", "Percentage")],
        default="fixed",
    )
    # Default value can be 'no'

    def __str__(self):
        return self.pricing_model_name


# Customer Tab 1: Account Information
class Customer(models.Model):
    customer_code = models.CharField(max_length=255, unique=True, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE, null=True)
    customer_type = models.ForeignKey(
        CustomerType,
        on_delete=models.CASCADE,
        null=True,
        related_name="customers_type_name",
    )
    company = models.ManyToManyField(Company, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    boro = models.CharField(max_length=255, null=True, blank=True)
    payment_terms = models.ForeignKey(PaymentTerms, on_delete=models.CASCADE, null=True)
    customer_group = models.ForeignKey(
        CustomerGroup, on_delete=models.CASCADE, null=True
    )
    credit_limit = models.IntegerField(null=True, blank=True)
    product_promotion = models.CharField(
        max_length=20, choices=[("yes", "Yes"), ("no", "No")], default="no"
    )
    customer_note = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_msa_include = models.BooleanField(default=False)
    is_sales_tax_applicable = models.BooleanField(default=False)
    send_email_on_invoice_creation = models.BooleanField(default=False)
    calculate_interest = models.BooleanField(default=False)
    self_checkout_tax = models.BooleanField(default=False)
    cash_and_carry_customer_code = models.BooleanField(default=False)

    # def save(self, *args, **kwargs):
    #     if not self.customer_code:  # Only generate on creation
    #         last_customer = Customer.objects.order_by("-id").first()
    #         if last_customer:
    #             last_code = int(last_customer.customer_code)  # Assuming numeric codes
    #             self.customer_code = str(last_code + 1).zfill(
    #                 6
    #             )  # e.g., '000001', '000002'
    #         else:
    #             self.customer_code = "000001"  # First entry

    #     super().save(*args, **kwargs)

    def generate_unique_code(self):
        """Generates a unique customer_code by incrementing the last highest numeric value."""
        last_customer = (
            Customer.objects.exclude(customer_code__isnull=True)
            .exclude(customer_code="")
            .order_by("-customer_code")
            .first()
        )

        if last_customer and last_customer.customer_code.isdigit():
            new_code = str(int(last_customer.customer_code) + 1).zfill(6)
        else:
            new_code = "000001"  # Default starting code

        return new_code

    def save(self, *args, **kwargs):
        if not self.customer_code:
            self.customer_code = self.generate_unique_code()

        while True:
            try:
                super().save(*args, **kwargs)
                break  # Successfully saved, exit loop
            except IntegrityError:  # Handle duplicate key error
                self.customer_code = str(int(self.customer_code) + 1).zfill(6)

    def __str__(self):
        return self.customer_name


class System(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Customer Tab 2: Pricing & Tax
class PricingAndTax(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        related_name="pricing_and_tax_models",
    )
    pricing_model_name = models.ForeignKey(PricingModel, on_delete=models.CASCADE)
    liquor_license_no = models.CharField(max_length=255, null=True, blank=True)
    tax_id = models.CharField(max_length=255, null=True, blank=True)
    tax_appeal = models.CharField(
        max_length=3,
        choices=[("yes", "Yes"), ("no", "No")],
        default="no",  # Default value can be 'no'
    )


# Customer Tab 3: Shipping & Billing Address
class ShippingBillingAddress(models.Model):
    address_type = models.CharField(
        max_length=255,
        choices=[
            (
                "shipping",
                "Shipping",
            ),
            (
                "billing",
                "Billing",
            ),
        ],
    )
    street_address = models.CharField(max_length=255)

    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    address_title = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        related_name="shipping_billing_addresses",
    )

    class Meta:
        unique_together = ("address_type", "customer")


# Customer Tab 4: Sec Information
class SecInformation(models.Model):
    cigar_license_number = models.CharField(max_length=255, null=True, blank=True)
    federal_license_number = models.CharField(max_length=255, null=True, blank=True)
    federal_expiry_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, related_name="sec_information"
    )
    credentials_for_customer_portal = models.BooleanField(
        default=False, null=True, blank=True
    )


class Vendor(models.Model):
    vendor_id = models.CharField(
        max_length=255,
        unique=True,
    )
    vendor_name = models.TextField(
        max_length=255,
    )
    contact_person_first_name = models.TextField(
        max_length=255,
    )
    contact_person_last_name = models.TextField(
        max_length=255,
    )

    def __str__(self):
        return self.vendor_name


class VendorSecondaryInformation(models.Model):
    minimum_order = models.CharField(max_length=255, null=True, blank=True)
    terms = models.TextField(
        max_length=255,
    )
    website = models.URLField(
        max_length=255,
    )
    account_number = models.CharField(
        max_length=255,
    )
    payment_discount = models.CharField(
        max_length=255,
    )
    minimum_order_quantity = models.CharField(
        max_length=255,
    )
    minimum_order_amount = models.CharField(
        max_length=255,
    )
    status = models.CharField(
        max_length=255,
        choices=[
            ("active", "Active"),
            ("in-active", "InActive"),
        ],
    )
    eft_customer = models.BooleanField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class VendorShippingBillingAddress(models.Model):
    address = models.CharField(max_length=255)

    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    mobile_no = models.CharField(max_length=20)  # Changed to CharField
    pager = models.CharField(max_length=20)  # Changed to CharField
    phone_number = models.CharField(max_length=20)  # Changed to CharField
    fax_no = models.CharField(max_length=20)  # Changed to CharField

    mailing_address = models.BooleanField(null=True, blank=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vendor.vendor_name} - {self.address}"


class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
    )
    vendor_po_number = models.CharField(max_length=100, unique=True)
    purchase_order_date = models.DateField()
    expected_delivery_date = models.DateField()
    delivery_status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Canceled", "Canceled"),
        ],
        default="Pending",
    )

    def __str__(self):
        return f"PO-{self.vendor_po_number} ({self.vendor.vendor_name})"


class Item(models.Model):
    upc_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="purchase_order_items"
    )
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Automatically calculate total cost
        self.total_cost = self.quantity * self.item.cost_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.item.name} for {self.purchase_order}"


class GoodsInward(models.Model):
    goods_inward_no = models.CharField(
        max_length=20, unique=True, verbose_name="Goods Inward No"
    )
    vendor_code = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Vendor Code"
    )
    vendor_name = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Vendor Name"
    )
    inward_date = models.DateField(verbose_name="Inward Date")
    purchase_order_no = models.CharField(
        max_length=20, verbose_name="Purchase Order No"
    )
    status = models.CharField(
        max_length=20,
        choices=[("Open", "Open"), ("Closed", "Closed")],
        default="Open",
        verbose_name="Status",
    )
    po_date = models.DateField(verbose_name="P/O Date")

    def __str__(self):
        return f"{self.goods_inward_no} - {self.purchase_order_no}"


class GoodsInwardItem(models.Model):
    goods_inward = models.ForeignKey(
        GoodsInward, on_delete=models.CASCADE, related_name="items"
    )
    item_code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    po_qty = models.FloatField()
    rec_qty = models.FloatField()
    case_qty = models.FloatField()

    def __str__(self):
        return f"Item {self.item_code} for {self.goods_inward.goods_inward_no}"


class Inventory(models.Model):
    purchase_invoice_number = models.CharField(max_length=20, unique=True)
    purchase_date = models.DateTimeField()
    section = models.CharField(max_length=100)
    is_price_updated = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.purchase_invoice_number}"


class InventoryItem(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="items"
    )
    item_number = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.item_number} ({self.item_name})"


class GoodsReceipt(models.Model):
    goods_receipt_date = models.DateField()
    invoice_number = models.CharField(max_length=20, unique=True)
    section = models.CharField(max_length=100)

    def __str__(self):
        return f"Receipt {self.invoice_number}"


class GoodsReceiptItem(models.Model):
    goods_receipt = models.ForeignKey(
        GoodsReceipt, on_delete=models.CASCADE, related_name="items"
    )
    item_number = models.CharField(max_length=100)
    item_name = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField()
    quantity_ordered = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item {self.item_number} ({self.item_name})"


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Employee Name")

    def __str__(self):
        return self.name


class Expense(models.Model):
    EXPENSE_PAYMENT_MODES = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
        # Add more payment modes as necessary
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Employee Name"
    )
    expense_name = models.CharField(max_length=100, verbose_name="Expense Name")
    payment_mode = models.CharField(
        max_length=50,
        choices=EXPENSE_PAYMENT_MODES,
        verbose_name="Expense Payment Mode",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Expense Amount"
    )
    expense_date = models.DateField(verbose_name="Expense Date")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return f"{self.expense_name} - {self.employee.name}"


# Sales_Order


class CustomerInformation(models.Model):
    name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=50)
    outstanding_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
    last_payment_date = models.DateField(null=True, blank=True)
    last_payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0
    )
    shipping_address = models.TextField()
    billing_address = models.TextField()
    cigarette_license_no = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class SalesOrder(models.Model):
    order_no = models.CharField(max_length=50, unique=True)
    ordered_by = models.CharField(max_length=255)
    order_date = models.DateField()
    delivery_date = models.DateField()
    delivery_type = models.CharField(
        max_length=50, choices=[("pickup", "Pickup"), ("delivery", "Delivery")]
    )
    order_comment = models.TextField(null=True, blank=True)
    customer_notes = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_po = models.CharField(max_length=50, null=True, blank=True)
    internal_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.order_no


class Department(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemInformation(models.Model):

    item_code = models.CharField(max_length=50)
    item_name = models.CharField(max_length=150, unique=True)
    units_of_measurement = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    primary_item_category = models.ForeignKey(
        ItemCategory, related_name="item_category", on_delete=models.CASCADE
    )

    weight = models.FloatField()  # Changed from CharField to FloatField
    vendor = models.ForeignKey(
        Vendor, related_name="item_vendor", on_delete=models.CASCADE
    )
    qty_per_unit = models.IntegerField()  # Changed from CharField to IntegerField
    quantity_on_hand = models.IntegerField()  # Changed from CharField to IntegerField
    manufacturer_item_no = models.CharField(max_length=50)
    # volume = models.FloatField()  # Changed from CharField to FloatField
    is_active = models.BooleanField(default=False)
    items_to_be_sold_by_units = models.BooleanField(default=False)
    company = models.ManyToManyField(Company)
    item_dimension = models.JSONField(max_length=50)

    def __str__(self):
        return self.item_name


class UPC(models.Model):

    upc_no = models.CharField(max_length=50, blank=True, null=True)
    box_upc = models.CharField(max_length=50, blank=True, null=True)
    inner_Pack_upc = models.CharField(max_length=50, blank=True, null=True)
    alternative_upc_1 = models.CharField(max_length=50, blank=True, null=True)
    alternative_upc_2 = models.CharField(max_length=50, blank=True, null=True)
    alternative_upc_3 = models.CharField(max_length=50, blank=True, null=True)
    item = models.ForeignKey(
        ItemInformation,
        related_name="upc_item",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.upc_no


class Brand(models.Model):

    brand_name = models.CharField(max_length=50)
    system = models.ForeignKey(
        System,
        related_name="brand_system",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.brand_name


class SecItemInformation(models.Model):
    secondary_item_no = models.CharField(max_length=50, blank=True, null=True)
    secondary_item_category = models.ForeignKey(
        ItemSecondaryCategory,
        related_name="secondary_item_category",
        on_delete=models.CASCADE,
    )
    expire_date = models.DateField()
    locations = models.CharField(
        max_length=50,
        choices=[("outside", "Outside"), ("inside", "Inside"), ("unknown", "Unknown")],
        default="unknown",
    )
    system = models.ManyToManyField(System, blank=True)
    brand = models.ForeignKey(
        Brand,
        related_name="second_item_brand",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    size = models.CharField(max_length=50, blank=True)

    item = models.ForeignKey(
        ItemInformation,
        related_name="second_item_item",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class ItemTax(models.Model):

    always_apply_tax_on_item = models.BooleanField(default=False)
    update_tax_for = models.CharField(
        max_length=18,
        choices=[
            ("all_companies", "All companies"),
            ("current_companies", "Current companies"),
            ("specific_companies", "Specific Companies"),
        ],
        default="all_companies",
    )
    taxable_by = models.CharField(
        max_length=18,
        choices=[
            ("price", "Price"),
            ("weight", "Weight"),
        ],
        default="price",
    )
    taxes = models.JSONField(null=True, blank=True)
    item = models.ForeignKey(
        ItemInformation,
        related_name="tax_item_item",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class MSAInformation(models.Model):
    PROMOTION_INDICATOR_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    include_in_msa = models.BooleanField(default=False)
    identification_symbol = models.CharField(max_length=50)
    distribution_sku = models.CharField(max_length=50)
    product_description = models.CharField(max_length=50)
    item_per_selling_unit = models.CharField(max_length=50)
    promotion_indicator = models.CharField(
        max_length=3,
        choices=PROMOTION_INDICATOR_CHOICES,
        default="no",
    )
    promotion_description = models.CharField(max_length=50)
    product_unit_size_description = models.CharField(max_length=50)
    msa_category_code = models.CharField(max_length=50)
    distributor_product_unit_size = models.CharField(max_length=50)

    item = models.ForeignKey(
        ItemInformation,
        related_name="msa_item_item",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def clean(self):
        # List of fields that should be required when include_in_msa is True
        required_fields = [
            "identification_symbol",
            "distribution_sku",
            "product_description",
            "item_per_selling_unit",
            "promotion_indicator",
            "promotion_description",
            "product_unit_size_description",
            "msa_category_code",
            "distributor_product_unit_size",
        ]

        # Check if include_in_msa is True and any of the required fields are empty
        if self.include_in_msa:
            for field in required_fields:
                if not getattr(self, field):  # Check if the field is empty
                    raise ValidationError(
                        {
                            field: f'{field.replace("_", " ").title()} is required when include_in_msa is selected.'
                        }
                    )

        super().clean()  # Ensure other validations are not skipped


class ItemCash(models.Model):

    is_cash_and_carry = models.BooleanField(default=False)
    cash_and_carry_item_code = models.CharField(max_length=50)
    item = models.ForeignKey(
        ItemInformation,
        related_name="item_cash_item",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class ItemPrice(models.Model):
    # apply_same_base_price_to_all_company = models.BooleanField(default=False)
    # apply_same_base_price_to_all_state = models.BooleanField(default=False)
    # prices = models.JSONField(null=True, blank=True)
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    margin = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    suggested_retail_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    suggested_min_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    suggested_max_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    promotion = models.CharField(
        max_length=50,
        choices=[
            ("none", "None"),
            ("offer", "Offer"),
            ("discount", "Discount"),
        ],
    )
    default = models.BooleanField(blank=True, null=True, default=True)
    item = models.ForeignKey(
        ItemInformation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class ItemVendor(models.Model):
    default_price = models.BooleanField(default=True)
    average = models.BooleanField(default=False)

    vendors = models.JSONField(null=True, blank=True)

    item = models.ForeignKey(
        ItemInformation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )


class OrderHistory(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    system = models.ForeignKey(System, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
    )
    section = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_number} - {self.customer.name}"


# InvoiceWithout Order for D&V Wholesale Inc.


class CustomerDetails(models.Model):
    name = models.CharField(max_length=255)
    last_payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    outstanding_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    def __str__(self):
        return self.name


class ItemDetails(models.Model):
    name = models.CharField(max_length=255)
    upc_code = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        ItemCategory, on_delete=models.CASCADE, related_name="items"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    excise_tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=100, unique=True, blank=True)
    cash_and_carry = models.BooleanField(blank=True, null=True)
    mark_as_paid = models.BooleanField(blank=True, null=True)
    invoice_date = models.DateTimeField(max_length=100, null=True)
    delivery_date = models.DateTimeField(max_length=100, null=True)
    po = models.TextField(max_length=100, null=True, blank=True)
    is_cash_and_carry_customer_code = models.BooleanField(blank=True, null=True)
    shipping_delivery_type = models.TextField(max_length=100, null=True)
    cash_and_carry_customer_code = models.TextField(
        max_length=100, null=True, blank=True
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    customer_type = models.ForeignKey(
        CustomerType, on_delete=models.CASCADE, related_name="invoices", null=True
    )
    salesman = models.ForeignKey(
        Salesman, on_delete=models.CASCADE, related_name="invoices", null=True
    )
    billing_address = models.TextField(blank=True, null=True)
    cigarette_license = models.TextField(blank=True, null=True)
    delivery_type = models.TextField(blank=True, null=True)
    customer_notes = models.TextField(blank=True, null=True)
    invoiceList = models.JSONField(blank=True, null=True)
    total_quantity = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_excise_tax = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    def save(self, *args, **kwargs):
        if not self.invoice_no:
            last_invoice = Invoice.objects.order_by("-id").first()
            if last_invoice and last_invoice.invoice_no:
                try:
                    last_number = int(last_invoice.invoice_no.split("-")[-1])
                except ValueError:
                    last_number = 0
            else:
                last_number = 0
            self.invoice_no = f"INV-{last_number + 1:04d}"  # INV-0001, INV-0002, etc.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_no}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoice_items"
    )
    item = models.ForeignKey(
        ItemDetails, on_delete=models.CASCADE
    )  # Corrected reference
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.item.name} on {self.invoice.invoice_no}"


# InvoiceHistory


class InvoiceType(models.Model):
    """
    Model for invoice types.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class InvoiceHistory(models.Model):
    """
    Model for invoices_history.
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="customer_history"
    )
    invoice_no = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ("Open", "Open"),
            ("Closed", "Closed"),
            ("Cancelled", "Cancelled"),
        ],
    )
    invoice_type = models.ForeignKey(
        InvoiceType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="invoices",
    )
    quantity = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_no} - {self.customer.name}"


class Tax(models.Model):
    tax_name = models.CharField(max_length=255)

    tax_by = models.CharField(
        max_length=255, choices=[("price", "Price"), ("weight", "Weight")]
    )
    tax_category = models.CharField(
        max_length=255,
        choices=[
            ("application-on-sales-tax", "Application on sales tax"),
            ("excise-tax", "excise tax"),
            ("product-tax", "product tax"),
        ],
    )

    additional_tax = models.CharField(
        max_length=255,
        choices=[("additional", "Additional"), ("included", "Included")],
        default="additional",
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.tax_name


class SpecialPricingClassification(models.Model):
    name = models.CharField(max_length=255, unique=True)
    expiry_date = models.CharField(max_length=255, null=True, blank=True)
    # is_expiration_date_apply = models.BooleanField(
    #     max_length=255, null=True, blank=True
    # )
    # update_price = models.BooleanField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class CustomerSpecialPricing(models.Model):
    price_classification = models.ForeignKey(
        SpecialPricingClassification, max_length=255, on_delete=models.CASCADE
    )
    item_no = models.CharField(max_length=255, null=True, blank=True)
    item_description = models.CharField(max_length=255, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    change_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    final_base_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    item_type = models.CharField(
        max_length=255,
        choices=[
            ("item", "Item"),
            ("item_category", "Item Category"),
            ("item_secondary_category", "Item secondary Category"),
            ("department", "Department"),
        ],
        null=True,
        blank=True,
    )
    # customer_id = models.CharField(max_length=255, null=True, blank=True)
    # customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_type = models.CharField(
        max_length=255,
        choices=[("customer", "Customer"), ("customer_group", "Customer Group")],
        null=True,
        blank=True,
    )
    selling_type = models.CharField(
        max_length=50,
        choices=[("selling", "Selling"), ("cost_price", "Cost Price")],
        null=True,
        blank=True,
    )
    price_type = models.CharField(
        max_length=50,
        choices=[("fixed", "Fixed"), ("percentage", "Percentage")],
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    item = models.ForeignKey(
        ItemInformation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    primary_category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    secondary_category = models.ForeignKey(
        ItemSecondaryCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # class Meta:
    #     constraints = [
    #         # Database level constraints if you want.
    #         models.UniqueConstraint(
    #             fields=["customer", "item"], name="unique_customer_item"
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer", "primary_category"],
    #             name="unique_customer_primary_category",
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer", "secondary_category"],
    #             name="unique_customer_secondary_category",
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer", "department"], name="unique_customer_department"
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer_group", "item"], name="unique_customer_group_item"
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer_group", "primary_category"],
    #             name="unique_customer_group_primary_category",
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer_group", "secondary_category"],
    #             name="unique_customer_group_secondary_category",
    #         ),
    #         models.UniqueConstraint(
    #             fields=["customer_group", "department"],
    #             name="unique_customer_group_department",
    #         ),
    #     ]

    # def clean(self):
    #     """Custom validation to ensure unique combinations."""
    #     errors = {}

    #     # Validate Customer based uniqueness
    #     if self.customer:
    #         if (
    #             self.item
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer=self.customer, item=self.item
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["item"] = "Combination of customer and item already exists."

    #         if (
    #             self.primary_category
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer=self.customer, primary_category=self.primary_category
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["primary_category"] = (
    #                 "Combination of customer and primary category already exists."
    #             )

    #         if (
    #             self.secondary_category
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer=self.customer, secondary_category=self.secondary_category
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["secondary_category"] = (
    #                 "Combination of customer and secondary category already exists."
    #             )

    #         if (
    #             self.department
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer=self.customer, department=self.department
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["department"] = (
    #                 "Combination of customer and department already exists."
    #             )

    #     # Validate CustomerGroup based uniqueness
    #     if self.customer_group:
    #         if (
    #             self.item
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer_group=self.customer_group, item=self.item
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["item"] = (
    #                 "Combination of customer group and item already exists."
    #             )

    #         if (
    #             self.primary_category
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer_group=self.customer_group,
    #                 primary_category=self.primary_category,
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["primary_category"] = (
    #                 "Combination of customer group and primary category already exists."
    #             )

    #         if (
    #             self.secondary_category
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer_group=self.customer_group,
    #                 secondary_category=self.secondary_category,
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["secondary_category"] = (
    #                 "Combination of customer group and secondary category already exists."
    #             )

    #         if (
    #             self.department
    #             and CustomerSpecialPricing.objects.filter(
    #                 customer_group=self.customer_group, department=self.department
    #             )
    #             .exclude(pk=self.pk)
    #             .exists()
    #         ):
    #             errors["department"] = (
    #                 "Combination of customer group and department already exists."
    #             )

    #     if errors:
    #         raise ValidationError(errors)

    # def save(self, *args, **kwargs):
    #     self.clean()  # Validation before save
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_no} - {self.item_description}"

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["item_no", "customer_id"], name="unique_item_customer"
    #         )
    #     ]

    # def clean(self):
    #     """Custom validation to check unique item_id and customer_id combination."""
    #     if self.item_no and self.customer_id:
    #         existing_record = CustomerSpecialPricing.objects.filter(
    #             item_no=self.item_no, customer_id=self.customer_id
    #         ).exclude(pk=self.pk)

    #         if existing_record.exists():
    #             raise ValidationError(
    #                 "A record with this item and customer already exists."
    #             )

    # def save(self, *args, **kwargs):
    #     """Call the clean method before saving."""
    #     self.clean()
    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.item_no} - {self.item_description}"
