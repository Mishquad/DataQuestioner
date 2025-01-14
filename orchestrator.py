from mistral_client import MistralWrapper
from data_analysis_agent import analyze_data_with_mistral
from hypothesis_generation_agent import generate_hypotheses_with_mistral
from hypothesis_validation_agent import validate_hypotheses_with_mistral
from save_pdf import generate_pdf

def orchestrate(base_data_path, current_data_path, api_key):
    # Initialize Mistral client
    mistral = MistralWrapper(api_key=api_key)

    try:
        # Step 1: Data Analysis
        discrepancies_summary = analyze_data_with_mistral(base_data_path, current_data_path, mistral)
        print("Analysis Summary:\n", discrepancies_summary)

        # Save analysis results to a file for later use
        with open("analysis_results.txt", "w") as file:
            file.write(discrepancies_summary)

        # Step 2: Hypothesis Generation
        hypotheses = generate_hypotheses_with_mistral(mistral)
        print("Generated Hypotheses:\n", hypotheses)

        # Save hypotheses to a file
        with open("hypotheses.txt", "w") as file:
            file.write("\n".join(hypotheses))

        # Step 3: Hypothesis Validation
        if not hypotheses:
            raise ValueError("No valid hypotheses generated or hypotheses is not a list.")

        validated_hypotheses = validate_hypotheses_with_mistral(mistral)
        print("Validated Hypotheses:\n", validated_hypotheses)

        # Save validated hypotheses to a file
        with open("validated_hypotheses.txt", "w") as file:
            file.write(validated_hypotheses)

        return {
            "analysis_summary": discrepancies_summary,
            "hypotheses": hypotheses,
            "validated_hypotheses": validated_hypotheses,
        }
    except Exception as e:
        print("An error occurred during orchestration:", str(e))
        return None

    final_result = {
            "Analysis Summary": discrepancies_summary,
            "Hypotheses": "\n".join(hypotheses),
            "Validated Hypotheses": "\n".join(validated_hypotheses)
        }
    generate_pdf(final_result)

