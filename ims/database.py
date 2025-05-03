import os
import django
import pandas as pd
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from ims.models import (
    Salesman, CompanyModel, CustomerType, PaymentTerms, CustomerGroup, ProductionPromotion,
    PricingModel, Customer, ProductPricingModel, PricingAndTaxModel, ShippingBillingAddress,
    SecInformation, Vendor, PurchaseOrder, Item, PurchaseOrderItem, GoodsInward, GoodsInwardItem,
    Inventory, InventoryItem, GoodsReceipt, GoodsReceiptItem
)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nish.settings')
django.setup()

# Define the path to your Excel file
EXCEL_FILE_PATH = r"D:\workspace\nish\nish_django_lcnc_backend\data\master_data.xlsx"

# Function to load data from a specific sheet
def load_data_from_sheet(sheet_name, model_class, field_mapping):
    try:
        data = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
        records = []
        
        for _, row in data.iterrows():
            record_data = {field: row[excel_column] for field, excel_column in field_mapping.items()}
            records.append(model_class(**record_data))
        
        # Bulk insert records for performance
        model_class.objects.bulk_create(records, ignore_conflicts=True)
        print(f"Loaded data for sheet: {sheet_name}")
    except Exception as e:
        print(f"Error loading data for sheet {sheet_name}: {e}")

# Main function to load data for all models
@transaction.atomic
def load_all_data():
    mappings = [
        {"sheet": "salesman", "model": Salesman, "fields": {"id": "id", "name": "name"}},
        {"sheet": "customer_company_name", "model": CompanyModel, "fields": {"id": "id", "name": "name"}},
        {"sheet": "customer_type", "model": CustomerType, "fields": {"id": "id", "type_name": "type_name"}},
        {"sheet": "payment_terms", "model": PaymentTerms, "fields": {"id": "id", "term_name": "term_name"}},
        {"sheet": "customer_group", "model": CustomerGroup, "fields": {"id": "id", "group_name": "group_name"}},
        {"sheet": "production_promotion", "model": ProductionPromotion, "fields": {"id": "id", "group_name": "group_name"}},
        {"sheet": "pricing_model", "model": PricingModel, "fields": {"id": "id", "name": "name"}},
        {"sheet": "customer", "model": Customer, "fields": {
            "id": "id", "customer_code": "customer_code", "customer_name": "customer_name",
            "contact_person_name": "contact_person_name", "salesman_id": "salesman_id", 
            "phone": "phone", "email": "email"
        }},
        {"sheet": "product_pricing_model", "model": ProductPricingModel, "fields": {"id": "id", "name": "name"}},
        {"sheet": "pricing_and_tax_model", "model": PricingAndTaxModel, "fields": {
            "customer_id": "customer_id", "liquor_license_no": "liquor_license_no",
            "pricing_model_name": "pricing_model_name", "tax_id": "tax_id", "tax_appeal": "tax_appeal"
        }},
        {"sheet": "shipping_billing_address", "model": ShippingBillingAddress, "fields": {
            "address_type": "address_type", "street_address": "street_address", "customer_id": "customer_id",
            "state": "state", "city": "city", "zip_code": "zip_code", "address_title": "address_title",
            "is_default": "is_default"
        }},
        {"sheet": "sec_information", "model": SecInformation, "fields": {
            "cigar_license_number": "cigar_license_number", "federal_license_number": "federal_license_number",
            "federal_expiry_date": "federal_expiry_date", "customer_id": "customer_id",
            "credentials_for_customer_portal": "credentials_for_customer_portal"
        }},
        {"sheet": "vendor", "model": Vendor, "fields": {"id": "id", "name": "name", "contact_info": "contact_info"}},
        {"sheet": "purchase_order", "model": PurchaseOrder, "fields": {
            "id": "id", "vendor_id": "vendor_id", "vendor_po_number": "vendor_po_number",
            "purchase_order_date": "purchase_order_date", "expected_delivery_date": "expected_delivery_date",
            "delivery_status": "delivery_status"
        }},
        {"sheet": "item", "model": Item, "fields": {
            "id": "id", "upc_code": "upc_code", "name": "name", "manufacturer": "manufacturer",
            "cost_price": "cost_price", "selling_price": "selling_price", "volume": "volume"
        }},
        {"sheet": "purchase_order_item", "model": PurchaseOrderItem, "fields": {
            "purchase_order_id": "purchase_order_id", "item_id": "item_id", "quantity": "quantity"
        }},
        {"sheet": "goods_inward", "model": GoodsInward, "fields": {
            "id": "id", "goods_inward_no": "goods_inward_no", "vendor_code": "vendor_code",
            "vendor_name": "vendor_name", "inward_date": "inward_date", "purchase_order_no": "purchase_order_no",
            "status": "status", "po_date": "po_date"
        }},
        {"sheet": "goods_inward_item", "model": GoodsInwardItem, "fields": {
            "goods_inward_id": "goods_inward_id", "item_code": "item_code", "description": "description",
            "po_qty": "po_qty", "rec_qty": "rec_qty", "case_qty": "case_qty"
        }},
        {"sheet": "inventory", "model": Inventory, "fields": {
            "id": "id", "purchase_invoice_number": "purchase_invoice_number",
            "purchase_date": "purchase_date", "section": "section", "is_price_updated": "is_price_updated",
            "created_by": "created_by", "updated_by": "updated_by"
        }},
        {"sheet": "inventory_item", "model": InventoryItem, "fields": {
            "inventory_id": "inventory_id", "item_number": "item_number", "item_name": "item_name",
            "quantity": "quantity", "selling_price": "selling_price"
        }},
        {"sheet": "goods_receipt", "model": GoodsReceipt, "fields": {
            "id": "id", "goods_receipt_date": "goods_receipt_date", "invoice_number": "invoice_number",
            "section": "section"
        }},
        {"sheet": "goods_receipt_item", "model": GoodsReceiptItem, "fields": {
            "goods_receipt_id": "goods_receipt_id", "item_number": "item_number",
            "item_name": "item_name", "quantity_in_stock": "quantity_in_stock",
            "quantity_ordered": "quantity_ordered", "price": "price"
        }},
    ]

    for mapping in mappings:
        load_data_from_sheet(mapping["sheet"], mapping["model"], mapping["fields"])

if __name__ == "__main__":
    load_all_data()



def create_salesman(name):
    """ Create a Salesman """
    salesman = Salesman.objects.create(name=name)
    return salesman

def create_company(name):
    """ Create a Company """
    company = CompanyModel.objects.create(name=name)
    return company

def create_customer(customer_code, customer_name, contact_person_name, phone, email, salesman):
    """ Create a Customer (One-to-Many relationship with Salesman) """
    customer = Customer.objects.create(
        customer_code=customer_code,
        customer_name=customer_name,
        contact_person_name=contact_person_name,
        phone=phone,
        email=email,
        salesman=salesman
    )
    return customer

def create_purchase_order(vendor, po_number, po_date, delivery_status="Pending"):
    """ Create a Purchase Order (One-to-Many relationship with Vendor) """
    po = PurchaseOrder.objects.create(
        vendor=vendor,
        vendor_po_number=po_number,
        purchase_order_date=po_date,
        delivery_status=delivery_status
    )
    return po

def create_goods_inward(purchase_order, inward_date, vendor_code, status="Open"):
    """ Create Goods Inward (One-to-Many relationship with Purchase Order) """
    goods_inward = GoodsInward.objects.create(
        goods_inward_no="GI" + str(purchase_order.id),
        vendor_code=vendor_code,
        purchase_order_no=purchase_order.vendor_po_number,
        inward_date=inward_date,
        status=status,
        po_date=purchase_order.purchase_order_date
    )
    return goods_inward

def add_items_to_purchase_order(purchase_order, items):
    """ Add Items to Purchase Order (Many-to-Many relationship with Item) """
    for item in items:
        PurchaseOrderItem.objects.create(
            purchase_order=purchase_order,
            item=item,
            quantity=item['quantity'],
            total_cost=item['total_cost']
        )

def get_customer_by_code(customer_code):
    """ Read Customer by code """
    try:
        customer = Customer.objects.get(customer_code=customer_code)
        return customer
    except ObjectDoesNotExist:
        return None

def update_customer_email(customer_code, new_email):
    """ Update a Customer's email """
    customer = get_customer_by_code(customer_code)
    if customer:
        customer.email = new_email
        customer.save()
        return customer
    return None

def delete_purchase_order(po_number):
    """ Delete a Purchase Order """
    try:
        purchase_order = PurchaseOrder.objects.get(vendor_po_number=po_number)
        purchase_order.delete()
        return True
    except ObjectDoesNotExist:
        return False

def get_all_customers():
    """ Get all customers (One-to-Many relationship retrieval) """
    return Customer.objects.all()

def get_all_purchase_orders():
    """ Get all Purchase Orders """
    return PurchaseOrder.objects.all()

def get_customer_orders(customer_code):
    """ Get all Purchase Orders for a Customer (One-to-Many relationship retrieval) """
    customer = get_customer_by_code(customer_code)
    if customer:
        return customer.purchase_orders.all()  # reverse relation using related_name
    return None

def create_vendor(name, contact_info=None):
    """ Create Vendor """
    vendor = Vendor.objects.create(name=name, contact_info=contact_info)
    return vendor

def create_item(upc_code, name, cost_price, selling_price, quantity=0):
    """ Create Item """
    item = Item.objects.create(
        upc_code=upc_code,
        name=name,
        cost_price=cost_price,
        selling_price=selling_price,
        volume=quantity
    )
    return item

def create_shipment_for_customer(customer_code, street_address, state, city, zip_code, address_title, is_default=False):
    """ Create Shipment or Billing Address for a Customer (One-to-Many relationship with Customer) """
    customer = get_customer_by_code(customer_code)
    if customer:
        shipping_address = ShippingBillingAddress.objects.create(
            customer=customer,
            address_type="Shipping",
            street_address=street_address,
            state=state,
            city=city,
            zip_code=zip_code,
            address_title=address_title,
            is_default=is_default
        )
        return shipping_address
    return None

def update_goods_inward_status(goods_inward_no, status):
    """ Update Goods Inward status """
    try:
        goods_inward = GoodsInward.objects.get(goods_inward_no=goods_inward_no)
        goods_inward.status = status
        goods_inward.save()
        return goods_inward
    except ObjectDoesNotExist:
        return None

def add_item_to_goods_inward(goods_inward_no, item_code, description, po_qty, rec_qty, case_qty):
    """ Add item to goods inward (Many-to-Many relationship with GoodsInward) """
    goods_inward = GoodsInward.objects.get(goods_inward_no=goods_inward_no)
    item = GoodsInwardItem.objects.create(
        goods_inward=goods_inward,
        item_code=item_code,
        description=description,
        po_qty=po_qty,
        rec_qty=rec_qty,
        case_qty=case_qty
    )
    return item

def many_to_many_relations():
    """ Example of Many-to-Many CRUD operations between Items and Purchase Orders """
    # Assuming you have items and purchase_orders already created
    purchase_order = PurchaseOrder.objects.first()  # Just an example, you would filter based on logic
    items = Item.objects.all()
    for item in items:
        PurchaseOrderItem.objects.create(
            purchase_order=purchase_order,
            item=item,
            quantity=5,
            total_cost=item.selling_price * 5
        )




# import os
# import django

# # Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nish.settings')
# django.setup()

# import os
# import pandas as pd
# from django.db import transaction
# from ims.models import (
#     Salesman, CompanyModel, CustomerType, PaymentTerms, CustomerGroup, ProductionPromotion,
#     PricingModel, Customer, ProductPricingModel, PricingAndTaxModel, ShippingBillingAddress,
#     SecInformation, Vendor, PurchaseOrder, Item, PurchaseOrderItem, GoodsInward, GoodsInwardItem,
#     Inventory, InventoryItem, GoodsReceipt, GoodsReceiptItem
# )

# # Define the path to your Excel file
# EXCEL_FILE_PATH = r"D:\workspace\nish\nish_django_lcnc_backend\data\master_data.xlsx"

# # Function to load data from a specific sheet
# def load_data_from_sheet(sheet_name, model_class, field_mapping):
#     try:
#         data = pd.read_excel(EXCEL_FILE_PATH, sheet_name=sheet_name)
#         records = []
        
#         for _, row in data.iterrows():
#             record_data = {field: row[excel_column] for field, excel_column in field_mapping.items()}
#             records.append(model_class(**record_data))
        
#         # Bulk insert records for performance
#         model_class.objects.bulk_create(records, ignore_conflicts=True)
#         print(f"Loaded data for sheet: {sheet_name}")
#     except Exception as e:
#         print(f"Error loading data for sheet {sheet_name}: {e}")

# # Main function to load data for all models
# @transaction.atomic
# def load_all_data():
#     mappings = [
#         {"sheet": "salesman", "model": Salesman, "fields": {"id": "id", "name": "name"}},
#         {"sheet": "customer_company_name", "model": CompanyModel, "fields": {"id": "id", "name": "name"}},
#         {"sheet": "customer_type", "model": CustomerType, "fields": {"id": "id", "type_name": "type_name"}},
#         {"sheet": "payment_terms", "model": PaymentTerms, "fields": {"id": "id", "term_name": "term_name"}},
#         {"sheet": "customer_group", "model": CustomerGroup, "fields": {"id": "id", "group_name": "group_name"}},
#         {"sheet": "production_promotion", "model": ProductionPromotion, "fields": {"id": "id", "group_name": "group_name"}},
#         {"sheet": "pricing_model", "model": PricingModel, "fields": {"id": "id", "name": "name"}},
#         {"sheet": "customer", "model": Customer, "fields": {
#             "id": "id", "customer_code": "customer_code", "customer_name": "customer_name",
#             "contact_person_name": "contact_person_name", "salesman_id": "salesman_id", 
#             "phone": "phone", "email": "email"
#         }},
#         {"sheet": "product_pricing_model", "model": ProductPricingModel, "fields": {"id": "id", "name": "name"}},
#         {"sheet": "pricing_and_tax_model", "model": PricingAndTaxModel, "fields": {
#             "customer_id": "customer_id", "liquor_license_no": "liquor_license_no",
#             "pricing_model_name": "pricing_model_name", "tax_id": "tax_id", "tax_appeal": "tax_appeal"
#         }},
#         {"sheet": "shipping_billing_address", "model": ShippingBillingAddress, "fields": {
#             "address_type": "address_type", "street_address": "street_address", "customer_id": "customer_id",
#             "state": "state", "city": "city", "zip_code": "zip_code", "address_title": "address_title",
#             "is_default": "is_default"
#         }},
#         {"sheet": "sec_information", "model": SecInformation, "fields": {
#             "cigar_license_number": "cigar_license_number", "federal_license_number": "federal_license_number",
#             "federal_expiry_date": "federal_expiry_date", "customer_id": "customer_id",
#             "credentials_for_customer_portal": "credentials_for_customer_portal"
#         }},
#         {"sheet": "vendor", "model": Vendor, "fields": {"id": "id", "name": "name", "contact_info": "contact_info"}},
#         {"sheet": "purchase_order", "model": PurchaseOrder, "fields": {
#             "id": "id", "vendor_id": "vendor_id", "vendor_po_number": "vendor_po_number",
#             "purchase_order_date": "purchase_order_date", "expected_delivery_date": "expected_delivery_date",
#             "delivery_status": "delivery_status"
#         }},
#         {"sheet": "item", "model": Item, "fields": {
#             "id": "id", "upc_code": "upc_code", "name": "name", "manufacturer": "manufacturer",
#             "cost_price": "cost_price", "selling_price": "selling_price", "volume": "volume"
#         }},
#         {"sheet": "purchase_order_item", "model": PurchaseOrderItem, "fields": {
#             "purchase_order_id": "purchase_order_id", "item_id": "item_id", "quantity": "quantity"
#         }},
#         {"sheet": "goods_inward", "model": GoodsInward, "fields": {
#             "id": "id", "goods_inward_no": "goods_inward_no", "vendor_code": "vendor_code",
#             "vendor_name": "vendor_name", "inward_date": "inward_date", "purchase_order_no": "purchase_order_no",
#             "status": "status", "po_date": "po_date"
#         }},
#         {"sheet": "goods_inward_item", "model": GoodsInwardItem, "fields": {
#             "goods_inward_id": "goods_inward_id", "item_code": "item_code", "description": "description",
#             "po_qty": "po_qty", "rec_qty": "rec_qty", "case_qty": "case_qty"
#         }},
#         {"sheet": "inventory", "model": Inventory, "fields": {
#             "id": "id", "purchase_invoice_number": "purchase_invoice_number",
#             "purchase_date": "purchase_date", "section": "section", "is_price_updated": "is_price_updated",
#             "created_by": "created_by", "updated_by": "updated_by"
#         }},
#         {"sheet": "inventory_item", "model": InventoryItem, "fields": {
#             "inventory_id": "inventory_id", "item_number": "item_number", "item_name": "item_name",
#             "quantity": "quantity", "selling_price": "selling_price"
#         }},
#         {"sheet": "goods_receipt", "model": GoodsReceipt, "fields": {
#             "id": "id", "goods_receipt_date": "goods_receipt_date", "invoice_number": "invoice_number",
#             "section": "section"
#         }},
#         {"sheet": "goods_receipt_item", "model": GoodsReceiptItem, "fields": {
#             "goods_receipt_id": "goods_receipt_id", "item_number": "item_number",
#             "item_name": "item_name", "quantity_in_stock": "quantity_in_stock",
#             "quantity_ordered": "quantity_ordered", "price": "price"
#         }},
#     ]

#     for mapping in mappings:
#         load_data_from_sheet(mapping["sheet"], mapping["model"], mapping["fields"])

# if __name__ == "__main__":
#     load_all_data()
