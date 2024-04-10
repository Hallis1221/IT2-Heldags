import pandas as pd
import numpy as np
import logging

from dataset.data_loader import DataLoader
class DataFramework:
    def __init__(self, filepath):
        self.df = DataLoader.load_data(filepath)

    def sort_column_string_by_length(self, column_name, ascending=True):
        logging.info(f"Sorting column '{column_name}' by length.")
        return self.df.sort_values(by=column_name, key=lambda col: col.str.len(), ascending=ascending)
    
    def sort_column_numeric(self, column_name, ascending=True):
        logging.info(f"Sorting column '{column_name}' numerically.")
        return self.df.sort_values(by=column_name, ascending=ascending)

    def filter_data(self, column_name, condition):
        logging.info(f"Filtering data based on {column_name}.")
        initial_count = len(self.df)
        newdf = self.df[self.df[column_name].apply(condition)]
        logging.info(f"Filtered down to {len(newdf)} rows from {initial_count} based on {column_name}.")
        return newdf

    def show_statistics(self):
        if self.df.empty:
            logging.warning("DataFrame is empty. No statistics to show.")
            return "DataFrame is empty. No statistics to show."
        else:
            return self.df.describe()
    
    def sample_data(self, n=5):
        logging.info(f"Sampling {n} random records from the dataset.")
        if len(self.df) < n:
            logging.warning("Sample size is larger than the dataset. Returning the whole dataset.")
            return self.df
        return self.df.sample(n)

    def advanced_filter(self, conditions):
        """
        Filter the DataFrame based on multiple conditions.
        Conditions should be a dictionary with column names as keys and (lambda) conditions as values.
        """
        mask = np.ones(len(self.df), dtype=bool)
        for col, condition in conditions.items():
            mask &= self.df[col].apply(condition)
        return self.df[mask]

    def auto_type_conversion(self):
        """
        Automatically convert columns to the most appropriate data types.
        """
        newDf = self.df.convert_dtypes()
        for col in newDf.columns:
            try:
                newDf[col] = pd.to_numeric(self.df[col], errors='ignore')
            except ValueError:
                pass
            try:
                newDf[col] = pd.to_datetime(self.df[col], errors='ignore')
            except ValueError:
                pass
        return newDf
    
    def sort_by_number_of_occurrences(self, column_name, ascending=True):
        logging.info(f"Sorting by number of occurrences in column '{column_name}'.")
        return self.df[column_name].value_counts().sort_values(ascending=ascending)
    
    def rename_column_values(self,column, valuesMap):
        logging.info(f"Renaming values in column '{column}'.")
        newDf = self.df.replace({column: valuesMap})
        logging.info(f"Values in column '{column}' have been renamed.")
        return newDf
    
    def find_closest_column_title(self, column_name):
        logging.info(f"Finding the closest column title to '{column_name}'.")
        allColumnNames = self.df.columns
        
        def similarity(s1, s2):
            if len(s1) > len(s2):
                s1, s2 = s2, s1
            if len(s2) == 0:
                return len(s1)
            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row
            return previous_row[-1]
        
        # assign a similarity score to each column name
        similarityScores = {}
        for col in allColumnNames:
            similarityScores[col] = similarity(column_name, col)

        # sort the column names by similarity score
        sortedColumns = sorted(similarityScores.items(), key=lambda x: x[1])

        logging.info(f"Closest column title to '{column_name}' is '{sortedColumns[0][0]}' with a similarity score of {sortedColumns[0][1]}.")
        return sortedColumns[0][0]
        