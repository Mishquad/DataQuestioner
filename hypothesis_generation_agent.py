import pandas as pd
from mistral_client import MistralWrapper

def generate_hypotheses(discrepancies):
    """
    Generates hypotheses and suggestions based on discrepancies.
    """
    hypotheses = []
    suggestions = []

    for column in discrepancies.columns.levels[0]:
        for index in discrepancies.index:
            if discrepancies[column].loc[index].isna().any():
                hypotheses.append(f"Data discrepancy found in column '{column}' at index {index}.")
                suggestions.append(f"Investigate the data in column '{column}' at index {index} for potential issues.")

    return hypotheses, suggestions

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate hypotheses based on discrepancies and send to Mistral.")
    parser.add_argument("--discrepancies", required=True, help="Path to the discrepancies CSV file.")
    parser.add_argument("--mistral-endpoint", required=True, help="Mistral API endpoint for sending hypotheses.")
    
    args = parser.parse_args()

    discrepancies = pd.read_csv(args.discrepancies)
    hypotheses, suggestions = generate_hypotheses(discrepancies)

    print("Generated Hypotheses:")
    for hypothesis in hypotheses:
        print(hypothesis)

    print("\nSuggestions:")
    for suggestion in suggestions:
        print(suggestion)

    # Send hypotheses and suggestions to Mistral
    mistral = MistralWrapper()
    response = mistral.send_data({"hypotheses": hypotheses, "suggestions": suggestions}, args.mistral_endpoint)

    print("Response from Mistral:")
    print(response)
