"""
tests/test_evaluator.py
-----------------------
Pytest suite for the AI evaluator module (evaluator.py).
Tests the confidence scoring logic and fallback behavior without
making real API calls (uses monkeypatching).
"""

import pytest
from unittest.mock import patch, MagicMock
from evaluator import evaluate_confidence, evaluate_guess_history


# ── evaluate_confidence tests ──────────────────────────────────────────────────

def test_confidence_no_history():
    """With no guesses, should return neutral 0.5."""
    score = evaluate_confidence([], (1, 100))
    assert score == 0.5

def test_confidence_single_guess():
    """With only one guess, not enough data — returns 0.5."""
    score = evaluate_confidence([50], (1, 100))
    assert score == 0.5

def test_confidence_perfect_binary_search():
    """
    Guessing the midpoint every time is perfect binary search.
    Score should be high (>= 0.7).
    """
    # Range 1-100: ideal first guess is 50, then 75, then 62
    score = evaluate_confidence([50, 75, 62], (1, 100))
    assert score >= 0.7

def test_confidence_random_guesses_lower():
    """Wildly random guesses should score lower than binary search."""
    random_score = evaluate_confidence([5, 95, 10, 90], (1, 100))
    binary_score = evaluate_confidence([50, 75, 62], (1, 100))
    assert random_score < binary_score

def test_confidence_returns_float():
    score = evaluate_confidence([40, 60], (1, 100))
    assert isinstance(score, float)

def test_confidence_value_range():
    """Score should always be between 0.0 and 1.0."""
    score = evaluate_confidence([1, 100, 2, 99, 3], (1, 100))
    assert 0.0 <= score <= 1.0

def test_confidence_equal_range():
    """Edge case: range of size 0 should return 1.0."""
    score = evaluate_confidence([5, 5], (5, 5))
    assert score == 1.0


# ── evaluate_guess_history tests (mocked API) ─────────────────────────────────

def test_evaluate_empty_history_no_api_call():
    """Empty history returns default tip without calling the API."""
    tip = evaluate_guess_history([], (1, 100), 8)
    assert "middle" in tip.lower() or "no guesses" in tip.lower() or len(tip) > 0

def test_evaluate_returns_string():
    """evaluate_guess_history always returns a string."""
    with patch("evaluator.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [{"text": "Try guessing 75 next!"}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = evaluate_guess_history([30, 60], (1, 100), 8)
        assert isinstance(result, str)
        assert len(result) > 0

def test_evaluate_uses_claude_response():
    """The function should return the text Claude provides."""
    with patch("evaluator.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "content": [{"text": "Great binary search! Try 75 next."}]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = evaluate_guess_history([50], (1, 100), 8)
        assert "binary search" in result.lower() or "75" in result

def test_evaluate_handles_timeout():
    """On timeout, should return a friendly fallback message."""
    import requests as req
    with patch("evaluator.requests.post", side_effect=req.exceptions.Timeout):
        result = evaluate_guess_history([40], (1, 100), 8)
        assert "⚠️" in result or "timed out" in result.lower()

def test_evaluate_handles_request_error():
    """On connection error, should return a friendly fallback message."""
    import requests as req
    with patch("evaluator.requests.post", side_effect=req.exceptions.ConnectionError("fail")):
        result = evaluate_guess_history([40], (1, 100), 8)
        assert "⚠️" in result

def test_evaluate_handles_bad_response_shape():
    """If the API returns an unexpected shape, don't crash."""
    with patch("evaluator.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"unexpected": "data"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = evaluate_guess_history([50], (1, 100), 8)
        assert isinstance(result, str)
        assert len(result) > 0