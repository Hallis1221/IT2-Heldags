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
    