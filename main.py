import logging
from dataset.data_cleaner import DataCleaner
from dataset.data_exporter import DataExporter
from dataset.main import DataFramework

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename="logs/data.log")

dataset_path = './data/HKS2023.csv'  # Adjust this to your dataset's path
framework = DataFramework(dataset_path)
datacleaner = DataCleaner()
framework.df = datacleaner.clean_data(framework.df)
framework.df = framework.filter_data("Gender", lambda x: x in ['M', 'F'])

grouped = framework.seperate_based_on_column("GroupdName")
for group, df in grouped.items():
    DataExporter.export_data(df, f"./data/pulje/{group}.xlsx", format='excel')
logging.info(framework.show_statistics())