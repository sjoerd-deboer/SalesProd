import SalesProd.constants as constants
import pandas as pd


class ParsedFile:
    file_name: str = None
    df: pd.DataFrame = None
    key_columns: list = None

    def __init__(self, file_name, key_columns, df):
        self.file_name = file_name
        self.key_columns = key_columns
        self.df = df

        if not self.check_for_unique_keys():
            print(f'Warning: {self.file_name} has duplicate keys')

    def drop_duplicates(self) -> bool:
        no_duplicates = True
        before_removal = self.df.shape[0]
        self.df.drop_duplicates(ignore_index=True, keep='first')
        after_removal = self.df.shape[0]
        if before_removal != after_removal:
            print(f'Removed {before_removal - after_removal} duplicate rows from {self.file_name}')
            no_duplicates = False
        return no_duplicates

    def check_for_unique_keys(self) -> bool:
        for key_column in self.key_columns:
            if not self.df[key_column].is_unique:
                return False
        return True

    def __str__(self):
        return f'ParsedFile({self.file_name}, {self.df.shape})'


class Parser:
    files: dict = None
    parsed_files: dict = None

    def __init__(self, files=None):
        if files is None:
            self.files = {}
        self.parsed_files = {}

    def add_file(self, table_name, file_name) -> None:
        self.files[table_name] = file_name

    def parse(self) -> dict:
        for table_name, file_name in self.files.items():
            print(f'Parsing {table_name} ({file_name})...')

            # Check if table is already parsed
            if table_name in self.parsed_files.keys():
                raise ValueError(f'File {table_name} already parsed; Remove from parsed_files before parsing again')

            # Parse file
            parsed_table = self.parse_file(table_name, file_name)
            print(f'Parsed {table_name} successfully: {parsed_table}')

        return self.parsed_files

    def parse_file(self, table_name, file_name) -> tuple:
        file_path = constants.DATA_DIR + file_name

        if table_name == constants.EMPLOYEE_TABLE:
            return self.parse_employee(file_path)
        elif table_name == constants.PRODUCT_TABLE:
            return self.parse_product_table(file_path)
        elif table_name == constants.PRODUCT_CATEGORY:
            return self.parse_product_category_table(file_path)
        elif table_name == constants.PRODUCT_SUB_CATEGORY:
            return self.parse_product_sub_category_table(file_path)
        elif table_name == constants.PRODUCT_VENDOR:
            return self.parse_product_vendor_table(file_path)
        elif table_name == constants.SALES_ORDER_DETAIL:
            return self.parse_sales_order_detail_table(file_path)

    def remove_parsed_file(self, table_name) -> None:
        if table_name in self.parsed_files.keys():
            del self.parsed_files[table_name]
        else:
            raise ValueError(f'File {table_name} not found in parsed_files')

    # ---- Table specific parse methods ----

    def parse_employee(self, file_path) -> tuple:
        column_names = ['employee_id', 'parent_id', 'first_name', 'last_name', 'middle_name', 'job_title', 'sales_territory',
                        'hire_date', 'birth_date', 'email_address', 'phone_number', 'marital_status',
                        'emergency_contact_name', 'emergency_contact_phone', 'salaried_flag', 'gender', 'pay_frequency',
                        'base_rate', 'vacation_hours', 'sick_leave_hours', 'current_flag', 'sales_person_flag',
                        'department_name', 'start_date', 'end_date', 'status']
        df = pd.read_csv(file_path, header=None, names=column_names, encoding='windows-1258')

        # Add df to parsed_files
        self.parsed_files[constants.EMPLOYEE_TABLE] = ParsedFile(file_path, constants.EMPLOYEE_TABLE_UNIQUE_COLUMNS, df)
        return df.shape

    def parse_product_table(self, file_path) -> tuple:
        column_names = ['product_id', 'name', 'product_number', 'make_flag', 'finished_goods_flag', 'color',
                        'safety_stock_level', 'reorder_point', 'standard_cost', 'list_price', 'size',
                        'size_unit_measure_code', 'weight_unit_measure_code', 'weight', 'days_to_manufacture',
                        'product_line', 'class', 'style', 'product_subcategory_id', 'product_model_id',
                        'sell_start_date', 'sell_end_date', 'discontinued_date']
        df = pd.read_csv(file_path, header=None, names=column_names, encoding='windows-1258')

        # Add df to parsed_files
        self.parsed_files[constants.PRODUCT_TABLE] = ParsedFile(file_path,
                                                                constants.PRODUCT_TABLE_UNIQUE_COLUMNS,
                                                                df)
        return df.shape

    def parse_product_category_table(self, file_path) -> tuple:
        column_names = ['product_category_id', 'name']
        df = pd.read_csv(file_path, header=None, names=column_names, encoding='windows-1258')

        # Add df to parsed_files
        self.parsed_files[constants.PRODUCT_CATEGORY] = ParsedFile(file_path,
                                                                   constants.PRODUCT_CATEGORY_UNIQUE_COLUMNS,
                                                                   df)
        return df.shape

    def parse_product_sub_category_table(self, file_path) -> tuple:
        column_names = ['product_sub_category_id', 'product_category_id', 'name']
        df = pd.read_csv(file_path, header=None, names=column_names, encoding='windows-1258')

        # Add df to parsed_files
        self.parsed_files[constants.PRODUCT_SUB_CATEGORY] = ParsedFile(file_path,
                                                                       constants.PRODUCT_SUB_CATEGORY_UNIQUE_COLUMNS,
                                                                       df)
        return df.shape

    def parse_product_vendor_table(self, file_path) -> tuple:
        column_names = ['product_id', 'vendor_id', 'average_lead_time', 'standard_price', 'last_receipt_cost',
                        'last_receipt_date', 'min_order_qty', 'max_order_qty', 'on_order_qty', 'unit_measure_code']
        df = pd.read_csv(file_path, header=None, names=column_names, encoding='windows-1258')

        # Add df to parsed_files
        self.parsed_files[constants.PRODUCT_VENDOR] = ParsedFile(file_path,
                                                                 constants.PRODUCT_VENDOR_UNIQUE_COLUMNS,
                                                                 df)
        return df.shape

    def parse_sales_order_detail_table(self, file_path) -> tuple:
        column_names = ['sales_order_id', 'sales_order_detail_id', 'product_id', 'special_offer_id', 'unit_price',
                        'order_qty', 'unit_price_discount', 'carrier_tracking_number', 'due_date', 'ship_date']
        df = pd.read_csv(file_path, header=None, names=column_names, encoding='windows-1258')

        # Add df to parsed_files
        self.parsed_files[constants.SALES_ORDER_DETAIL] = ParsedFile(file_path,
                                                                     constants.SALES_ORDER_DETAIL_UNIQUE_COLUMNS,
                                                                     df)
        return df.shape
