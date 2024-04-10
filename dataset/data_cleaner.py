import pandas as pd
import logging

class DataCleaner:
    @staticmethod
    def clean_data(df, critical_columns =  ['Bib', 'Firstname', 'Surname', 'Gender', 'Nation']):
        logging.info("Cleaning data...")
        initial_count = len(df)
        df.dropna(subset=critical_columns, inplace=True)
        logging.info(f"Removed {initial_count - len(df)} rows with NaN values in critical columns.")

        df.columns = df.columns.str.replace('"', '')
        return df
    
    def remove_if_missing_any(self, df):
        """
        Remove rows with missing values in any columns (as long as atleast one row contains it
        """
        logging.info("Removing rows with missing values in any column...")
        initial_count = len(df)
        df.dropna(inplace=True)
        logging.info(f"Removed {initial_count - len(df)} rows with missing values in any column.")
        return df

    
    def remove_duplicates(self, df):
        logging.info("Removing duplicates...")
        initial_count = len(df)
        df.drop_duplicates(inplace=True)
        logging.info(f"Removed {initial_count - len(df)} duplicate rows.")
        return df
    
    def remove_outliers(self, df, columns, z_threshold=3):
        logging.info("Removing outliers...")
        initial_count = len(df)
        for col in columns:
            df = df[(df[col] - df[col].mean()).abs() <= z_threshold * df[col].std()]
        logging.info(f"Removed {initial_count - len(df)} outliers.")
        return df