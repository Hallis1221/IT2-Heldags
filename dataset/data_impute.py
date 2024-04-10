import pandas as pd

class DataImputer:
    def __init__(self, strategy='median'):
        self.strategy = strategy

    def impute(self, df):
        if self.strategy not in ['median', 'mean', 'mode']:
            raise ValueError(f"Unknown strategy {self.strategy}")

        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                if self.strategy == 'median':
                    df[col].fillna(df[col].median(), inplace=True)
                elif self.strategy == 'mean':
                    df[col].fillna(df[col].mean(), inplace=True)
                elif self.strategy == 'mode':
                    df[col].fillna(df[col].mode()[0], inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
        return df
    
    def impute_advanced(self, strategy='median'):
        """
        Impute missing values with a specified strategy: 'median', 'mean', or 'mode' for numeric columns.
        """
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                if strategy == 'median':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                elif strategy == 'mean':
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
                elif strategy == 'mode':
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
            else:
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)