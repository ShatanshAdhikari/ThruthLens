"""
Pipeline accuracy benchmark.

Tests the full CAR pipeline against claims with known ground-truth verdicts.
Requires Ollama running and at least one search source configured.

Run:
    pytest backend/tests/test_accuracy.py -v -s

The suite prints a precision/recall/F1 report at the end and asserts that
overall accuracy meets a minimum threshold (ACCURACY_FLOOR).
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ACCURACY_FLOOR = 0.60  # minimum fraction of claims labelled correctly

# (input_text, expected_status)
BENCHMARK: list[tuple[str, str]] = [
    # --- Should be Supported ---
    ("The Eiffel Tower is located in Paris, France.", "Supported"),
    ("The Pacific Ocean is the largest ocean on Earth.", "Supported"),
    ("William Shakespeare was an English playwright and poet.", "Supported"),
    ("Mount Everest is the highest mountain above sea level.", "Supported"),
    ("Python programming language was first released in 1991.", "Supported"),
    ("Vatican City is the smallest country in the world by area.", "Supported"),
    ("Photosynthesis is the process plants use to convert light into chemical energy.", "Supported"),

    # --- Should be Contradicted ---
    ("The Eiffel Tower was built in 1950.", "Contradicted"),
    ("Albert Einstein failed mathematics as a child.", "Contradicted"),
    ("The Great Wall of China is clearly visible from space with the naked eye.", "Contradicted"),
    ("Python programming language was created by James Gosling.", "Contradicted"),
    ("Mount Everest is located in Africa.", "Contradicted"),
    ("Vatican City is located in Germany.", "Contradicted"),

    # --- Ambiguous / Insufficient Evidence (acceptable: Inconclusive OR Insufficient Evidence) ---
    ("Coffee consumption increases workplace productivity by exactly 30%.", "Inconclusive"),
    ("The average person has exactly 7 dreams per night.", "Inconclusive"),
]

# Statuses where "Inconclusive" and "Insufficient Evidence" are both acceptable
_INCONCLUSIVE_GROUP = {"Inconclusive", "Insufficient Evidence"}


def _verdict_matches(actual: str, expected: str) -> bool:
    if expected in _INCONCLUSIVE_GROUP:
        return actual in _INCONCLUSIVE_GROUP
    return actual == expected


def _call_pipeline(text: str) -> str:
    response = client.post("/api/verify", json={"text": text}, timeout=120)
    assert response.status_code == 200, f"HTTP {response.status_code} for: {text}"
    data = response.json()
    if not data.get("claims"):
        return "No Claims"
    return data["claims"][0]["status"]


@pytest.mark.parametrize("claim,expected", BENCHMARK)
def test_single_claim_accuracy(claim: str, expected: str):
    actual = _call_pipeline(claim)
    assert _verdict_matches(actual, expected), (
        f"\nClaim:    {claim}\n"
        f"Expected: {expected}\n"
        f"Got:      {actual}"
    )


def test_overall_accuracy_report():
    """
    Runs the full benchmark and prints a labelled accuracy report.
    Fails if overall accuracy falls below ACCURACY_FLOOR.
    """
    correct = 0
    rows = []

    for claim, expected in BENCHMARK:
        actual = _call_pipeline(claim)
        ok = _verdict_matches(actual, expected)
        correct += int(ok)
        rows.append((ok, expected, actual, claim))

    total = len(BENCHMARK)
    accuracy = correct / total

    # Per-label precision / recall
    labels = ["Supported", "Contradicted", "Inconclusive"]

    def stats(label):
        tp = sum(1 for ok, exp, act, _ in rows if ok and exp == label)
        fp = sum(1 for ok, exp, act, _ in rows if not ok and act == label)
        fn = sum(1 for ok, exp, act, _ in rows if not ok and exp == label)
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall    = tp / (tp + fn) if (tp + fn) else 0.0
        f1        = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
        return precision, recall, f1

    print("\n" + "=" * 72)
    print(f"  TruthLens Accuracy Benchmark  —  {correct}/{total} correct ({accuracy:.0%})")
    print("=" * 72)
    print(f"  {'Label':<26} {'Precision':>9} {'Recall':>9} {'F1':>9}")
    print("-" * 72)
    for label in labels:
        p, r, f = stats(label)
        print(f"  {label:<26} {p:>8.0%}  {r:>8.0%}  {f:>8.0%}")
    print("=" * 72)
    print("\n  Failures:")
    for ok, exp, act, claim in rows:
        if not ok:
            print(f"  [FAIL] expected={exp:<18} got={act:<18} '{claim[:60]}'")
    print()

    assert accuracy >= ACCURACY_FLOOR, (
        f"Accuracy {accuracy:.0%} is below the required floor of {ACCURACY_FLOOR:.0%}"
    )
