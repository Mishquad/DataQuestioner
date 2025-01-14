import pandas as pd
from mistral_client import MistralWrapper

from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_data_with_mistral(base_data_path, current_data_path, mistral_wrapper):
    prompt = (
        "You are a data analyst. Compare the following datasets and summarize discrepancies, including NaNs, patterns, "
        "and irregular values:\n\n"
        f"Base Data Path: {base_data_path}\nCurrent Data Path: {current_data_path}\n\n"
        "You can make all permutations with data. But no python code for output allowed!"
        "Provide a summary of discrepancies as plain text. Make sure column names are displayed correctly."
    )
    analysis_result = mistral_wrapper.generate_completion(prompt)
    
    # Save output to a text file
    with open("analysis_results.txt", "w") as file:
        file.write(analysis_result or "No discrepancies found.")
    
    return analysis_result
