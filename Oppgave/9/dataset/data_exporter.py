import logging

class DataExporter:
    @staticmethod
    def export_data(df, file_path, format='csv'):
        try:
            if format == 'csv':
                df.to_csv(file_path, index=False)
            elif format == 'excel':
                df.to_excel(file_path, index=False)
            elif format == 'json':
                df.to_json(file_path, orient='records')
            else:
                raise ValueError("Unsupported format. Please choose 'csv', 'excel', or 'json'.")
            logging.info(f"Data exported successfully to {file_path}.")
        except Exception as e:
            logging.error(f"Failed to export data: {e}")
