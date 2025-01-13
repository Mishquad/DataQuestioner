from mistral_client import MistralWrapper
from data_analysis_agent import analyze_data
from hypothesis_generation_agent import generate_hypotheses
from hypothesis_validation_agent import validate_hypotheses


def orchestrate(base_data_path, current_data_path, api_key):
    # Initialize Mistral wrapper
    mistral = MistralWrapper(api_key=api_key)

    # Analyze discrepancies
    discrepancies = analyze_data(base_data_path, current_data_path)

    # Generate hypotheses
    hypotheses, suggestions = generate_hypotheses(discrepancies)

    # Validate hypotheses
    validated_hypotheses = validate_hypotheses(hypotheses)

    # Use Mistral to summarize or process hypotheses
    model = "codestral-latest"
    prompt = "\n".join(validated_hypotheses)
    suffix = "\n\nSuggestions:\n" + "\n".join(suggestions)

    response = mistral.generate_completion(
        model=model,
        prompt=prompt,
        suffix=suffix,
        temperature=0.7,
        top_p=0.9,
    )

    print("Mistral Response:")
    print(response)

    return response
