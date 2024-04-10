import pandas as pd
import logging

class DataLoader:
    @staticmethod
    def load_data(filepath):
        logging.info("Loading data...")
        try:
            df = pd.read_csv(filepath)
            logging.info(f"Initial dataset loaded with {len(df)} records.")
            return df
        except Exception as e:
            logging.error(f"Failed to load data: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on failure
