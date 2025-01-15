import pandas as pd
from mistral_client import MistralWrapper
import numpy as np

def preprocess_data(file_path):
    """Load and clean dataset."""
    try:
        df = pd.read_csv(file_path)
        df.dropna(inplace=True)  # Remove rows with missing values
        return df
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {e}")

def calculate_psi(base_array, current_array, bins=10):
    """Calculate Population Stability Index (PSI) for a numeric column."""
    base_hist, bin_edges = np.histogram(base_array, bins=bins, density=True)
    current_hist, _ = np.histogram(current_array, bins=bin_edges, density=True)

    psi_values = []
    for b, c in zip(base_hist, current_hist):
        if b > 0 and c > 0:  # Avoid division by zero
            psi_values.append((b - c) * np.log(b / c))
    return sum(psi_values)

def compare_datasets(base_df, current_df):
    """Compare base and current datasets to find discrepancies."""
    report = []

    numeric_columns = base_df.select_dtypes(include=['number']).columns
    categorical_columns = base_df.select_dtypes(exclude=['number']).columns

    for column in numeric_columns:
        base_stats = base_df[column].describe()
        current_stats = current_df[column].describe()

        discrepancies = {
            "mean_diff": current_stats['mean'] - base_stats['mean'],
            "max_diff": current_stats['max'] - base_stats['max'],
            "min_diff": current_stats['min'] - base_stats['min'],
            "q1_diff": current_stats['25%'] - base_stats['25%'],
            "q3_diff": current_stats['75%'] - base_stats['75%'],
            "psi": calculate_psi(base_df[column], current_df[column]),
        }
        
        if any(abs(value) > 0 for value in discrepancies.values()):
            report.append(f"Numeric column '{column}': {discrepancies}")

    for column in categorical_columns:
        base_freq = base_df[column].value_counts(normalize=True)
        current_freq = current_df[column].value_counts(normalize=True)
        
        freq_diff = (current_freq - base_freq).dropna()
        significant_changes = freq_diff[abs(freq_diff) > 0.1]  # Threshold for significant change

        if not significant_changes.empty:
            report.append(f"Categorical column '{column}': {significant_changes.to_dict()}")

    return "\n".join(report)

def analyze_data_with_rag(base_data_path, current_data_path, mistral_wrapper):
    """Enhanced analysis using RAG."""
    base_df = preprocess_data(base_data_path)
    current_df = preprocess_data(current_data_path)

    discrepancies_summary = compare_datasets(base_df, current_df)

    retrieval_context = (
        f"Discrepancies Summary:\n{discrepancies_summary}\n\n"
        "Examples:\n"
    )

    # Add specific examples to the retrieval context
    examples = []
    for column in base_df.columns:
        if column in base_df.select_dtypes(include=['number']).columns:
            base_example = base_df[column].sample(1).iloc[0]
            current_example = current_df[column].sample(1).iloc[0]
            examples.append(f"Numeric column '{column}': base example {base_example}, current example {current_example}")
        else:
            base_example = base_df[column].value_counts().idxmax()
            current_example = current_df[column].value_counts().idxmax()
            examples.append(f"Categorical column '{column}': base example '{base_example}', current example '{current_example}'")

    retrieval_context += "\n".join(examples)

    prompt = (
        "You are a data analyst using RAG to analyze datasets. Use the provided context to summarize insights.\n\n"
        f"Context:\n{retrieval_context}\n\n"
        "Focus on identifying changed distributions, unusual behavior, and provide proof for each insight based on the examples."
        "It is important to keep specific metric like mean or median in the output."
    )

    analysis_result = mistral_wrapper.generate_completion(prompt)

    with open("analysis_results.txt", "w") as file:
        file.write(analysis_result or "No discrepancies found.")

    return analysis_result

# Example usage (uncomment and set paths for real execution)
# mistral_wrapper = MistralWrapper()
# result = analyze_data_with_rag('base_1_16k.csv', 'current_data.csv', mistral_wrapper)
# print(result)
