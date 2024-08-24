import pandas as pd
import json

def clean_data(df):
    # 1. Fill NaN values with an empty string or any other value
    df = df.fillna("")

    # 2. Optionally, ensure all data is converted to string type (to avoid issues with mixed types)
    df = df.astype(str)

    return df

def convert_csv_to_data(file_name):
    try:
        # 1. Read the CSV file with a specified encoding
        df = pd.read_csv(file_name, encoding='ISO-8859-1')

        # Clean the data
        df = clean_data(df)

        # 2. Convert DataFrame to a list of lists
        data = df.values.tolist()

        # Optionally, include headers if you want to add them to the sheet
        headers = df.columns.values.tolist()
        data.insert(0, headers)  # Add headers as the first row

        # 3. Save the converted data to a JSON file
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)

        print("Data converted and saved to data.json")
    except Exception as e:
        print(f"Error: {e}")




if __name__ == "__main__":
    # Change 'yourfile.csv' to the path of your CSV file
    convert_csv_to_data('samplecsv.csv')
