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
