import constants
from Services.Parser import Parser, ParsedFile


def remove_duplicates(pf: dict) -> None:
    print('Removing duplicates...')
    for table_name, parsed_file in pf.items():
        parsed_file.drop_duplicates()


def merge_dates(file: ParsedFile) -> None:
    print('Merging dates...')
    df = file.df
    df_new = df.groupby(['employee_id'], as_index=False).first()
    file.df = df_new

    if not file.check_for_unique_keys():
        raise ValueError(f'Error: {file.file_name} has duplicate keys after merging dates')


if __name__ == '__main__':
    parser = Parser()

    parser.add_file(constants.EMPLOYEE_TABLE, constants.EMPLOYEE_TABLE_FILE)
    parser.add_file(constants.PRODUCT_TABLE, constants.PRODUCT_TABLE_FILE)
    parser.add_file(constants.PRODUCT_CATEGORY, constants.PRODUCT_CATEGORY_FILE)
    parser.add_file(constants.PRODUCT_SUB_CATEGORY, constants.PRODUCT_SUB_CATEGORY_FILE)
    parser.add_file(constants.SALES_ORDER_DETAIL, constants.SALES_ORDER_DETAIL_FILE)
    parser.parse()

    # Remove duplicate rows
    remove_duplicates(parser.parsed_files)
    # Merge dates in the employee table
    merge_dates(parser.parsed_files[constants.EMPLOYEE_TABLE])


