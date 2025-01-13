from mistral_client import MistralWrapper

def validate_hypotheses(hypotheses):
    """
    Validates hypotheses by appending a 'Validated' tag.
    """
    validated_hypotheses = [f"{hypothesis} - Validated" for hypothesis in hypotheses]
    return validated_hypotheses

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate hypotheses and send to Mistral.")
    parser.add_argument("--input", required=True, help="Path to the file containing hypotheses (one per line).")
    parser.add_argument("--mistral-endpoint", required=True, help="Mistral API endpoint for sending validated hypotheses.")
    
    args = parser.parse_args()

    with open(args.input, "r") as f:
        hypotheses = [line.strip() for line in f.readlines()]

    validated_hypotheses = validate_hypotheses(hypotheses)

    print("Validated Hypotheses:")
    for hypothesis in validated_hypotheses:
        print(hypothesis)

    # Send validated hypotheses to Mistral
    mistral = MistralWrapper()
    response = mistral.send_data({"validated_hypotheses": validated_hypotheses}, args.mistral_endpoint)

    print("Response from Mistral:")
    print(response)
