import pandas as pd
from mistral_client import MistralWrapper

from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns

base_df = pd.read_csv('base_1_16k.csv')

def analyze_data_with_mistral(base_data_path, current_data_path, mistral_wrapper):

    prompt = (
        "You are a data analyst. Compare two following datasets and summarize discrepancies, including NaNs, patterns, "
        "and irregular values:\n\n"
        f"Base Data Path: {base_data_path}\nCurrent Data Path: {current_data_path}\n\n"
        "Columns in both frames are the same and in order:transaction_time, transaction_qty, store_id, store_location, product_id, unit_price, product_category, product_type, product_detail"
        "You can make all permutations with data. But no python code for output allowed!"
        "Provide a summary of discrepancies as plain text, provide ratios and examples if suitable.\n\n"
        "Focus on changed distribution, unusual behaviour in current data compared to base data."
        "But limit your response only to the provided data."
    )
    analysis_result = mistral_wrapper.generate_completion(prompt)
    
    # Save output to a text file
    with open("analysis_results.txt", "w") as file:
        file.write(analysis_result or "No discrepancies found.")
    
    return analysis_result
