import pandas as pd
from mistral_client import MistralWrapper

def analyze_and_send_to_mistral(base_data_path, current_data_path):
    from data_analysis_agent import analyze_data

    discrepancies = analyze_data(base_data_path, current_data_path)

    mistral = MistralWrapper()
    response = mistral.send_data({"discrepancies": discrepancies.to_dict()}, "/analyze_data")

    print("Response from Mistral:")
    print(response)


def analyze_data(base_data_path, current_data_path):
    """
    Compares two CSV datasets and returns discrepancies.
    """
    base_data = pd.read_csv(base_data_path)
    current_data = pd.read_csv(current_data_path)
    discrepancies = base_data.compare(current_data)
    return discrepancies

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze discrepancies between two CSV datasets.")
    parser.add_argument("--base", required=True, help="Path to the base data CSV file.")
    parser.add_argument("--current", required=True, help="Path to the current data CSV file.")
    parser.add_argument("--output", help="Path to save discrepancies as a CSV file.", default=None)

    args = parser.parse_args()

    discrepancies = analyze_data(args.base, args.current)
    print("Discrepancies found:")
    print(discrepancies)

    if args.output:
        discrepancies.to_csv(args.output)
        print(f"Discrepancies saved to {args.output}.")