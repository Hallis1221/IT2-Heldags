import logging
from dataset.data_cleaner import DataCleaner
from dataset.data_exporter import DataExporter
from dataset.main import DataFramework

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename="logs/data.log")

dataset_path = './data/HKS2023.csv'  # Adjust this to your dataset's path
framework = DataFramework(dataset_path)
framework.df = DataCleaner.clean_data(framework.df)
DataExporter.export_data(framework.df, './data/cleaned_data.csv')
DataExporter.export_data(framework.df, './data/cleaned_data.xlsx', format='excel')
DataExporter.export_data(framework.df, './data/cleaned_data.json', format='json')

logging.info("Sorted by the number of occurrences in 'Firstname':")
logging.info(framework.sort_by_number_of_occurrences('Firstname', ascending=False))

logging.info("Sorted by the number of occurrences in 'Surname':")
logging.info(framework.sort_by_number_of_occurrences('Surname', ascending=False))
# visualization of nations in a pie chart
classAgeFrom = framework.find_closest_column_title('ClassAgeFrom')
framework.df = framework.filter_data(classAgeFrom, lambda x: 18 <= x <= 25)
logging.info(framework.sample_data(10))