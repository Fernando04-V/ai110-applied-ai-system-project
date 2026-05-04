"""
tests/test_evaluator.py
-----------------------
Pytest suite for the rule-based AI coach in evaluator.py.
All tests are fully local — no API calls, no mocking required.
History entries are (guess, outcome) tuples matching the format stored by app.py.
"""

import pytest
from evaluator import evaluate_confidence, evaluate_guess_history


# ── evaluate_confidence ────────────────────────────────────────────────────────

def test_confidence_no_history():
    """Not enough data — returns neutral 0.5."""
    assert evaluate_confidence([], (1, 100)) == 0.5

def test_confidence_single_guess():
    """Only one guess — not enough data, returns 0.5."""
    assert evaluate_confidence([(50, "Too Low")], (1, 100)) == 0.5

def test_confidence_perfect_binary_search():
    """Guessing near the midpoint each time should score high."""
    score = evaluate_confidence(
        [(50, "Too Low"), (75, "Too High"), (62, "Win")], (1, 100)
    )
    assert score >= 0.7

def test_confidence_random_scores_lower_than_binary():
    """Random guesses should score lower than binary search."""
    random_score = evaluate_confidence(
        [(5, "Too Low"), (95, "Too High"), (10, "Too Low"), (90, "Too High")], (1, 100)
    )
    binary_score = evaluate_confidence(
        [(50, "Too Low"), (75, "Too High"), (62, "Win")], (1, 100)
    )
    assert random_score < binary_score

def test_confidence_returns_float():
    score = evaluate_confidence([(40, "Too Low"), (60, "Win")], (1, 100))
    assert isinstance(score, float)

def test_confidence_always_between_0_and_1():
    score = evaluate_confidence(
        [(1, "Too Low"), (100, "Too High"), (2, "Too Low"), (99, "Too High"), (3, "Too Low")],
        (1, 100)
    )
    assert 0.0 <= score <= 1.0

def test_confidence_equal_range_returns_1():
    """Edge case: range of size 0 should not crash and returns 1.0."""
    score = evaluate_confidence([(5, "Win"), (5, "Win")], (5, 5))
    assert score == 1.0


# ── evaluate_guess_history ─────────────────────────────────────────────────────

def test_empty_history_returns_string():
    result = evaluate_guess_history([], (1, 100), 8)
    assert isinstance(result, str)
    assert len(result) > 0

def test_empty_history_suggests_midpoint():
    result = evaluate_guess_history([], (1, 100), 8)
    assert "middle" in result.lower() or "range" in result.lower()

def test_single_good_guess_near_midpoint():
    """A first guess near 50 should get positive feedback."""
    result = evaluate_guess_history([(50, "Too Low")], (1, 100), 8)
    assert "start" in result.lower() or "middle" in result.lower() or "great" in result.lower()

def test_single_bad_guess_far_from_midpoint():
    """A first guess far from the midpoint should suggest the midpoint."""
    result = evaluate_guess_history([(5, "Too Low")], (1, 100), 8)
    assert "50" in result or "midpoint" in result.lower() or "consider" in result.lower()

def test_repeated_guess_detected():
    """Repeating a number should trigger a warning."""
    result = evaluate_guess_history(
        [(50, "Too Low"), (30, "Too Low"), (50, "Too High")], (1, 100), 8
    )
    assert "twice" in result.lower() or "same" in result.lower()

def test_tiny_steps_detected():
    """Guessing in tiny increments should trigger the small steps warning."""
    result = evaluate_guess_history(
        [(50, "Too Low"), (51, "Too Low"), (52, "Too Low"), (53, "Too Low")], (1, 100), 8
    )
    assert "small" in result.lower() or "steps" in result.lower() or "jump" in result.lower()

def test_low_attempts_urgent_tip():
    """With only 1 attempt left the coach should be urgent."""
    result = evaluate_guess_history(
        [(10, "Too Low"), (90, "Too High"), (30, "Too Low"),
         (70, "Too High"), (40, "Too Low"), (60, "Too High"), (45, "Too Low")],
        (1, 100), 8
    )
    assert "left" in result.lower() or "attempt" in result.lower()

def test_binary_search_detected():
    """Clean binary search guesses should get positive feedback."""
    result = evaluate_guess_history(
        [(50, "Too Low"), (75, "Too High"), (62, "Win")], (1, 100), 8
    )
    assert "binary" in result.lower() or "solid" in result.lower() or "efficient" in result.lower()

def test_random_guesses_get_tip():
    """Random-looking guesses should get a suggestion to try the midpoint."""
    result = evaluate_guess_history(
        [(15, "Too Low"), (90, "Too High"), (22, "Too Low")], (1, 100), 8
    )
    assert "random" in result.lower() or "systematic" in result.lower() or "50" in result

def test_always_returns_string():
    """evaluate_guess_history must always return a string, no crashes."""
    for history in [
        [],
        [(1, "Too Low")],
        [(1, "Too Low"), (99, "Too High")],
        [(50, "Too Low"), (25, "Too High"), (75, "Too High"), (12, "Too Low")],
    ]:
        result = evaluate_guess_history(history, (1, 100), 8)
        assert isinstance(result, str)
        assert len(result) > 0

def test_easy_difficulty_range():
    """Coach should work correctly on Easy range 1-20."""
    result = evaluate_guess_history([(10, "Too Low")], (1, 20), 6)
    assert isinstance(result, str)

def test_hard_difficulty_range():
    """Coach should work correctly on Hard range 1-50."""
    result = evaluate_guess_history([(25, "Too Low"), (37, "Too High")], (1, 50), 5)
    assert isinstance(result, str)
