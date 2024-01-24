# Data Path
DATA_DIR = 'data/'

# Employee
EMPLOYEE_TABLE = 'employee'
EMPLOYEE_TABLE_FILE = 'Employee.txt'
EMPLOYEE_TABLE_UNIQUE_COLUMNS = ['employee_id']
EMPLOYEE_TABLE_COLUMN_NAMES = ['employee_id', 'parent_id', 'first_name', 'last_name', 'middle_name', 'job_title',
                               'sales_territory', 'hire_date', 'birth_date', 'email_address', 'phone_number',
                               'marital_status', 'emergency_contact_name', 'emergency_contact_phone', 'salaried_flag',
                               'gender', 'pay_frequency', 'base_rate', 'vacation_hours', 'sick_leave_hours',
                               'current_flag', 'sales_person_flag', 'department_name', 'start_date', 'end_date',
                               'status']

# Product
PRODUCT_TABLE = 'product'
PRODUCT_TABLE_FILE = 'Product.txt'
PRODUCT_TABLE_UNIQUE_COLUMNS = ['product_id']
PRODUCT_TABLE_COLUMN_NAMES = ['product_id', 'name', 'product_number', 'make_flag', 'finished_goods_flag', 'color',
                              'safety_stock_level', 'reorder_point', 'standard_cost', 'list_price', 'size',
                              'size_unit_measure_code', 'weight_unit_measure_code', 'weight', 'days_to_manufacture',
                              'product_line', 'class', 'style', 'product_subcategory_id', 'product_model_id',
                              'sell_start_date', 'sell_end_date', 'discontinued_date']

# ProductCategory
PRODUCT_CATEGORY = 'product-category'
PRODUCT_CATEGORY_FILE = 'ProductCategory.txt'
PRODUCT_CATEGORY_UNIQUE_COLUMNS = ['product_category_id']
PRODUCT_CATEGORY_COLUMN_NAMES = ['product_category_id', 'name']

# ProductSubCategory
PRODUCT_SUB_CATEGORY = 'product-sub-category'
PRODUCT_SUB_CATEGORY_FILE = 'ProductSubcategory.txt'
PRODUCT_SUB_CATEGORY_UNIQUE_COLUMNS = ['product_sub_category_id']
PRODUCT_SUB_CATEGORY_COLUMN_NAMES = ['product_sub_category_id', 'product_category_id', 'name']

# ProductVendor
PRODUCT_VENDOR = 'product-vendor'
PRODUCT_VENDOR_FILE = 'ProductVendor.txt'
PRODUCT_VENDOR_UNIQUE_COLUMNS = ['vendor_id']
PRODUCT_VENDOR_COLUMN_NAMES = ['product_id', 'vendor_id', 'average_lead_time', 'standard_price', 'last_receipt_cost',
                               'last_receipt_date', 'min_order_qty', 'max_order_qty', 'on_order_qty',
                               'unit_measure_code']

# SalesOrderDetail
SALES_ORDER_DETAIL = 'sales-order-detail'
SALES_ORDER_DETAIL_FILE = 'SalesOrderDetail.txt'
SALES_ORDER_DETAIL_UNIQUE_COLUMNS = ['sales_order_detail_id']
SALES_ORDER_DETAIL_COLUMN_NAMES = ['sales_order_id', 'sales_order_detail_id', 'product_id', 'special_offer_id',
                                   'unit_price','order_qty', 'unit_price_discount', 'carrier_tracking_number',
                                   'due_date', 'ship_date']

# SalesOrderHeader
SALES_ORDER_HEADER = 'sales-order-header'
SALES_ORDER_HEADER_FILE = 'SalesOrderHeader.csv'
SALES_ORDER_HEADER_UNIQUE_COLUMNS = ['sales_order_id']
SALES_ORDER_HEADER_COLUMN_NAMES = ['sales_order_id', 'revision_number', 'order_date', 'due_date', 'ship_date', 'status',
                                   'online_order_flag', 'purchase_order_number', 'account_number', 'customer_id',
                                   'salesperson_id', 'territory_id', 'bill_to_address_id', 'ship_to_address_id',
                                   'ship_method_id', 'creditcard_id', 'creditcard_approval_code', 'currency_rate_id',
                                   'subtotal', 'tax_amt', 'freight', 'total_due', 'comment', 'row_guid',
                                   'modified_date']

# SalesTerritory
SALES_TERRITORY = 'sales-territory'
SALES_TERRITORY_FILE = 'SalesTerritory.csv'
SALES_TERRITORY_UNIQUE_COLUMNS = ['territory_id']
SALES_TERRITORY_COLUMN_NAMES = ['territory_id', 'name', 'country_region_code', 'group', 'sales_ytd', 'sales_last_year',
                                'cost_ytd', 'cost_last_year', 'row_guid', 'modified_date']

# SpecialOffer
SPECIAL_OFFER = 'special-offer'
SPECIAL_OFFER_FILE = 'SpecialOffer.csv'
SPECIAL_OFFER_UNIQUE_COLUMNS = ['special_offer_id']
SPECIAL_OFFER_COLUMN_NAMES = ['special_offer_id', 'description', 'discount_pct', 'type', 'category', 'start_date',
                              'end_date', 'min_qty', 'max_qty', 'row_guid', 'modified_date']