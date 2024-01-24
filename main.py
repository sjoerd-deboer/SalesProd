import pandas as pd

import constants
from SalesProd.Services.Enricher import Enricher
from Services.Parser import Parser, ParsedFile
from pandas import DataFrame
from tqdm import tqdm
from sqlalchemy import create_engine

tqdm.pandas()


def remove_duplicates(pf: dict) -> None:
    print('Removing duplicates in all files...')
    for table_name, parsed_file in pf.items():
        parsed_file.drop_duplicates()


def merge_dates(file: ParsedFile) -> None:
    print(f'Merging records with duplicate keys for {constants.EMPLOYEE_TABLE}...')
    df = file.df
    df_new = df.groupby(['employee_id'], as_index=False).first()
    file.df = df_new

    if not file.check_for_unique_keys():
        raise ValueError(f'Error: {file.file_name} has duplicate keys after merging dates')


def create_employee_table(p: Parser) -> pd.DataFrame:
    print(f'Creating Employee table...')
    pf = p.parsed_files
    employee_df = pf[constants.EMPLOYEE_TABLE].df

    new_df = DataFrame()
    new_df['employeeID'] = employee_df['employee_id']
    new_df['name'] = employee_df['first_name'] + ' ' + employee_df['last_name']
    new_df['gender'] = employee_df['gender']
    new_df['department'] = employee_df['department_name']
    new_df['function'] = employee_df['job_title']
    new_df['maritalStatus'] = employee_df['marital_status']
    new_df['hireDate'] = employee_df['hire_date']
    new_df['vacationHours'] = employee_df['vacation_hours']
    new_df['sickLeaveHours'] = employee_df['sick_leave_hours']

    return new_df


def create_sales_territory_table(p: Parser) -> pd.DataFrame:
    print(f'Creating SalesTerritory table...')
    pf = p.parsed_files
    sales_territory_df = pf[constants.SALES_TERRITORY].df

    new_df = DataFrame()
    new_df['territoryID'] = sales_territory_df['territory_id']
    new_df['name'] = sales_territory_df['name']

    return new_df


def create_special_offer_table(p: Parser) -> pd.DataFrame:
    print(f'Creating SpecialOffer table...')
    pf = p.parsed_files
    special_offer_df = pf[constants.SPECIAL_OFFER].df

    new_df = DataFrame()
    new_df['specialOfferID'] = special_offer_df['special_offer_id']
    new_df['description'] = special_offer_df['description']
    new_df['discountPct'] = special_offer_df['discount_pct']
    new_df['type'] = special_offer_df['type']
    new_df['category'] = special_offer_df['category']

    return new_df


def create_product_category_table(p: Parser) -> pd.DataFrame:
    print(f'Creating ProductCategory table...')
    pf = p.parsed_files
    product_category_df = pf[constants.PRODUCT_CATEGORY].df

    new_df = DataFrame()
    new_df['productCategoryID'] = product_category_df['product_category_id']
    new_df['name'] = product_category_df['name']

    return new_df


def create_product_subcategory_table(p: Parser) -> pd.DataFrame:
    print(f'Creating ProductSubcategory table...')
    pf = p.parsed_files
    product_subcategory_df = pf[constants.PRODUCT_SUB_CATEGORY].df

    new_df = DataFrame()
    new_df['productSubcategoryID'] = product_subcategory_df['product_sub_category_id']
    new_df['productCategoryID'] = product_subcategory_df['product_category_id']
    new_df['name'] = product_subcategory_df['name']

    return new_df


def create_product_table(p: Parser) -> pd.DataFrame:
    print(f'Creating Product table...')
    pf = p.parsed_files
    product_df = pf[constants.PRODUCT_TABLE].df

    new_df = DataFrame()
    new_df['productID'] = product_df['product_id']
    new_df['productSubcategoryID'] = product_df['product_subcategory_id']
    new_df['name'] = product_df['name']
    new_df = convert_column_to_numeric(new_df, ['productSubcategoryID'])

    return new_df


def create_sales_order_detail_table(p: Parser) -> pd.DataFrame:
    print(f'Creating SalesOrderDetail table...')
    pf = p.parsed_files
    sales_order_detail_df = pf[constants.SALES_ORDER_DETAIL].df
    sales_order_detail_df = sales_order_detail_df[['sales_order_detail_id', 'sales_order_id', 'product_id',
                                                   'special_offer_id', 'order_qty', 'unit_price_discount',
                                                   'order_date']]
    sales_order_detail_df = convert_column_to_numeric(sales_order_detail_df,
                                                      ['sales_order_detail_id', 'sales_order_id', 'product_id',
                                                       'special_offer_id'])
    # Merge with sales_order_header_df to get territory_id
    sales_order_header_df = pf[constants.SALES_ORDER_HEADER].df

    sales_order_header_df = sales_order_header_df[['sales_order_id', 'territory_id']]
    merged_df = pd.merge(sales_order_detail_df, sales_order_header_df, left_on='sales_order_id',
                         right_on='sales_order_id', how='inner')
    merged_df = convert_column_to_numeric(merged_df, ['territory_id'])

    # Calculate the season based on the order_date
    merged_df['season'] = merged_df.progress_apply(lambda row: get_season(row['order_date'], p, row['territory_id']),
                                                   axis=1)
    new_df = DataFrame()
    new_df['salesOrderDetailID'] = merged_df['sales_order_detail_id']
    new_df['salesOrderID'] = merged_df['sales_order_id']
    new_df['productID'] = merged_df['product_id']
    new_df['specialOfferID'] = merged_df['special_offer_id']
    new_df['territoryID'] = merged_df['territory_id']
    new_df['orderQty'] = merged_df['order_qty']
    new_df['unitPriceDiscount'] = merged_df['unit_price_discount']
    new_df['orderDate'] = merged_df['order_date']
    new_df['season'] = merged_df['season']

    return new_df


def convert_column_to_numeric(df: pd.DataFrame, column_names: list) -> pd.DataFrame:
    df_copy = df.copy()
    for column_name in column_names:
        print(f'Converting {column_name} to numeric...')
        df_copy[column_name] = pd.to_numeric(df[column_name], errors='coerce', downcast='integer')
        # Handle NaN values
        df_copy[column_name] = df_copy[column_name].fillna(0).astype(int)
        # Convert to integers explicitly
        df_copy[column_name] = df_copy[column_name].astype(int, errors='ignore')
    return df_copy


def get_season(order_date: pd.Timestamp, p: Parser, territory_id: int) -> str:
    month = order_date.month
    seasons_df = p.parsed_files[constants.SEASONS].df
    seasons_df = seasons_df[seasons_df['month'] == month]
    if territory_id == 9:
        season = seasons_df[seasons_df['location'] == 'southern hemisphere']
    else:
        season = seasons_df[seasons_df['location'] == 'northern hemisphere']
    temp = season['season'].iloc[0]
    return temp


if __name__ == '__main__':
    # Connecting to the database
    driver = 'postgresql'
    username = 'dab_ds23241a_144'
    dbname = username
    password = 'f8QXeCZAEsgAclBZ'
    server = 'bronto.ewi.utwente.nl'
    port = '5432'
    engine = create_engine(f'{driver}://{username}:{password}@{server}:{port}/{dbname}')

    # Parse files
    parser = Parser()
    parser.add_file(constants.EMPLOYEE_TABLE, constants.EMPLOYEE_TABLE_FILE)
    parser.add_file(constants.PRODUCT_TABLE, constants.PRODUCT_TABLE_FILE)
    parser.add_file(constants.PRODUCT_CATEGORY, constants.PRODUCT_CATEGORY_FILE)
    parser.add_file(constants.PRODUCT_SUB_CATEGORY, constants.PRODUCT_SUB_CATEGORY_FILE)
    parser.add_file(constants.SALES_ORDER_DETAIL, constants.SALES_ORDER_DETAIL_FILE)
    parser.add_file(constants.SALES_ORDER_HEADER, constants.SALES_ORDER_HEADER_FILE)
    parser.add_file(constants.SALES_TERRITORY, constants.SALES_TERRITORY_FILE)
    parser.add_file(constants.SPECIAL_OFFER, constants.SPECIAL_OFFER_FILE)
    parser.add_file(constants.SEASONS, constants.SEASONS_FILE)
    parser.parse()

    # Remove duplicate rows
    remove_duplicates(parser.parsed_files)

    # Merge dates in the employee table
    merge_dates(parser.parsed_files[constants.EMPLOYEE_TABLE])

    # Enrich data
    enricher = Enricher(parser.parsed_files)
    enricher.calculate_sales_date()

    # Create tables
    employee_table = create_employee_table(parser)
    sales_territory_table = create_sales_territory_table(parser)
    special_offer_table = create_special_offer_table(parser)
    product_category_table = create_product_category_table(parser)
    product_subcategory_table = create_product_subcategory_table(parser)
    product_table = create_product_table(parser)
    sales_order_detail_table = create_sales_order_detail_table(parser)

    # Adding the employee to the database
    print('Adding the employee to the database...')
    employee_table.to_sql('employee', engine, schema='Project_DEP', index=False, if_exists='replace')
    # Adding the product to the database
    print('Adding the product to the database...')
    product_table.to_sql('product', engine, schema='Project_DEP', index=False, if_exists='replace')
    # Adding the productcategory to the database
    print('Adding the productcategory to the database...')
    product_category_table.to_sql('productcategory', engine, schema='Project_DEP', index=False, if_exists='replace')
    # Adding the productsubcategory to the database
    print('Adding the productsubcategory to the database...')
    product_subcategory_table.to_sql('productsubcategory', engine, schema='Project_DEP', index=False,
                                     if_exists='replace')
    # Adding the salesorderdetail to the database
    print('Adding the salesorderdetail to the database...')
    sales_order_detail_table.to_sql('salesorderdetail', engine, schema='Project_DEP', index=False, if_exists='replace')
    # Adding the salesterritory to the database
    print('Adding the salesterritory to the database...')
    sales_territory_table.to_sql('salesterritory', engine, schema='Project_DEP', index=False, if_exists='replace')
    # Adding the specialoffer to the database
    print('Adding the specialoffer to the database...')
    special_offer_table.to_sql('specialoffer', engine, schema='Project_DEP', index=False, if_exists='replace')
