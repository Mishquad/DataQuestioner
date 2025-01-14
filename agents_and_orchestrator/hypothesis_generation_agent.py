from mistral_client import MistralWrapper

def generate_hypotheses_with_mistral(mistral_wrapper):
    # Read the analysis results from the pre-defined file
    try:
        with open("analysis_results.txt", "r") as file:
            analysis_results = file.read()
    except FileNotFoundError:
        raise ValueError("The analysis_results.txt file was not found. Ensure the Data Analysis Agent has run successfully.")

    if not analysis_results.strip():
        raise ValueError("No analysis results found in analysis_results.txt.")

    prompt = (
        "You are a hypothesis generator. Based on the following discrepancies, generate hypotheses and suggestions:\n\n"
        f"{analysis_results}\n\n"
        "Provide hypotheses and suggestions in two separate sections: Hypotheses and Suggestions."
        "Answer should be as plain text."
    )
    hypothesis_result = mistral_wrapper.generate_completion(prompt)

    # Split and save hypotheses and suggestions
    if "Suggestions:" in hypothesis_result:
        hypotheses, suggestions = hypothesis_result.split("Suggestions:")
    else:
        hypotheses = hypothesis_result
        suggestions = ""

    with open("hypotheses.txt", "w") as hypo_file:
        hypo_file.write(hypotheses)
    with open("suggestions.txt", "w") as sugg_file:
        sugg_file.write(suggestions)
    
    return hypotheses, suggestions