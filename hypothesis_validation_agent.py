from mistral_client import MistralWrapper

def validate_hypotheses_with_mistral(mistral_wrapper):
    # Read the hypotheses from the pre-defined file
    try:
        with open("hypotheses.txt", "r") as file:
            hypotheses = file.readlines()
    except FileNotFoundError:
        raise ValueError("The hypotheses.txt file was not found. Ensure the Hypothesis Generation Agent has run successfully.")

    if not hypotheses:
        raise ValueError("No hypotheses found in hypotheses.txt.")

    prompt = (
        "You are a validation expert. Validate the following hypotheses and provide explanations:\n\n"
        f"{''.join(hypotheses)}\n\n"
        "Provide validated hypotheses with explanations."
    )
    validation_result = mistral_wrapper.generate_completion(prompt)

    # Save validated hypotheses
    with open("validated_hypotheses.txt", "w") as file:
        file.write(validation_result)
    
    return validation_result





