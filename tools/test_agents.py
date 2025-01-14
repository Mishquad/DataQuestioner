import pandas as pd
from data_analysis_agent import analyze_data
from hypothesis_generation_agent import generate_hypotheses
from hypothesis_validation_agent import validate_hypotheses

def test_analyze_data():
    base_data = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    current_data = pd.DataFrame({"A": [1, 2, 0], "B": [4, 0, 6]})

    base_data.to_csv("test_base.csv", index=False)
    current_data.to_csv("test_current.csv", index=False)

    discrepancies = analyze_data("test_base.csv", "test_current.csv")

    assert not discrepancies.empty, "Discrepancies should not be empty."

def test_generate_hypotheses():
    discrepancies = pd.DataFrame({
        ("A", "self"): [None, None, 3],
        ("A", "other"): [None, None, 0],
        ("B", "self"): [None, 5, None],
        ("B", "other"): [None, 0, None],
    })

    hypotheses, suggestions = generate_hypotheses(discrepancies)

    assert len(hypotheses) > 0, "Hypotheses should not be empty."
    assert len(suggestions) > 0, "Suggestions should not be empty."

def test_validate_hypotheses():
    hypotheses = ["Data discrepancy in column 'A' at index 2."]
    validated_hypotheses = validate_hypotheses(hypotheses)

    assert len(validated_hypotheses) == len(hypotheses), "All hypotheses should be validated."
    assert "Validated" in validated_hypotheses[0], "Validated hypothesis should include the term 'Validated'."
