import pandas as pd
from sklearn.preprocessing import StandardScaler
import random
import string

# Function to anonymize column names (optional)
def anonymize_column_names(df):
    anonymized_columns = {col: f"col_{i+1}" for i, col in enumerate(df.columns)}
    df = df.rename(columns=anonymized_columns)
    return df

# Function to scale numerical data using Standard Scaler
def scale_numerical_data(df):
    scaler = StandardScaler()

    # Select only numerical columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df

# Function to anonymize string columns (optional transformation)
def anonymize_string_columns(df):
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = [''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) for _ in range(len(df))]
    return df

# Function to save transformed data to a new CSV file
def save_transformed_data(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Transformed data saved to {output_path}")

# Main function to process and transform the data
def process_and_transform_data(input_path, output_path, anonymize_columns=False, scale_data=True):
    # Load data from CSV file
    df = pd.read_csv(input_path)
    
    # Optionally anonymize column names
    if anonymize_columns:
        df = anonymize_column_names(df)
    
    # Scale numerical data (StandardScaler)
    if scale_data:
        df = scale_numerical_data(df)
    
    # Optionally anonymize string columns (replace sensitive text data)
    df = anonymize_string_columns(df)
    
    # Save the transformed data to a new file
    save_transformed_data(df, output_path)

if __name__ == "__main__":
    # Example usage
    input_file_path = 'your_input_data.csv'  # Replace with your actual input file path
    output_file_path = 'transformed_data_scaled.csv'  # The path to save transformed data
    process_and_transform_data(input_file_path, output_file_path)
