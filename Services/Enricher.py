from datetime import timedelta
import SalesProd.constants as constants
import pandas as pd


class Enricher:
    parsed_files: dict = None

    def __init__(self, parsed_files: dict):
        self.parsed_files = parsed_files

    def calculate_sales_date(self, file_name: str = constants.SALES_ORDER_DETAIL,
                             date_column: str = 'due_date', new_column: str = 'order_date') -> None:
        print(f'Calculating {new_column} column for {file_name}...')
        df = self.parsed_files[file_name].df

        # Ensure date_column is in datetime format
        df[date_column] = pd.to_datetime(df[date_column])

        # Calculate new_column by subtracting 12 days from 'due_date'
        df[new_column] = df[date_column] - timedelta(days=12)

        # Assign the new dataframe to the parsed file object
        self.parsed_files[file_name].df = df

    # TODO: add longitute and latitude columns to SalesTerritory
    # TODO: add temperature column to SalesOrderDetail
