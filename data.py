import logging
import pandas as pd
from dataset.data_cleaner import DataCleaner
from dataset.main import DataFramework

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    filename="logs/data.log")

# Initialize paths and classes
dataset_path = './data/googleplaystore.csv' 
framework = DataFramework(dataset_path)
datacleaner = DataCleaner()

# Clean data
framework.df = datacleaner.clean_data(framework.df, critical_columns=[])

# Drop duplicate entries based on 'App' name and set 'App' as the index
framework.df = framework.df.drop_duplicates(subset='App').set_index('App')

# Convert Reviews column to numeric and sort
framework.df['Reviews'] = pd.to_numeric(framework.df['Reviews'], errors='coerce')
framework.df = framework.df.sort_values(by='Reviews', ascending=False)

# Clean and convert Rating and Installs columns
framework.df['Rating'] = pd.to_numeric(framework.df['Rating'], errors='coerce').fillna(3.0)
framework.df['Installs'] = framework.df['Installs'].str.replace('+', '').str.replace(',', '')
framework.df['Installs'] = pd.to_numeric(framework.df['Installs'], errors='coerce').fillna(0)

# Get the top 3 categories by app count
top_categories = framework.df['Category'].value_counts().head(3).index

# Process each top category
for category in top_categories:
    category_df = framework.df[framework.df['Category'] == category].drop_duplicates()

    # Calculate average rating and installs
    average_rating = category_df['Rating'].mean()
    average_installs = category_df['Installs'].mean()

    # Get top 3 most installed apps
    most_installed_apps = category_df.nlargest(3, 'Installs')[['Rating', 'Installs']]

    # Log results
    logging.info(f"Category: {category}")
    logging.info(f"Average rating: {average_rating:.2f}")
    logging.info(f"Average installs: {average_installs:.2f}")
    logging.info(f"Top 3 most installed apps:\n{most_installed_apps}")

    # Print results to console
    print(f"Category: {category}")
    print(f"Average rating: {average_rating:.2f}")
    print(f"Average installs: {average_installs:.2f}")
    print("Top 3 most installed apps:")
    print(most_installed_apps.to_string(index=True))
    print()
