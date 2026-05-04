"""
tests/test_game_logic.py
------------------------
Pytest suite for core game logic in logic_utils.py.
Tests check_guess, parse_guess, update_score, and get_range_for_difficulty.
"""
 
import pytest
from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty
 
 
# ── check_guess ────────────────────────────────────────────────────────────────
 
def test_check_guess_win():
    outcome, msg = check_guess(42, 42)
    assert outcome == "Win"
 
def test_check_guess_too_high():
    outcome, msg = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in msg
 
def test_check_guess_too_low():
    outcome, msg = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in msg
 
def test_check_guess_boundary_low():
    outcome, _ = check_guess(1, 1)
    assert outcome == "Win"
 
def test_check_guess_boundary_high():
    outcome, _ = check_guess(100, 100)
    assert outcome == "Win"
 
def test_check_guess_off_by_one_above():
    outcome, _ = check_guess(51, 50)
    assert outcome == "Too High"
 
def test_check_guess_off_by_one_below():
    outcome, _ = check_guess(49, 50)
    assert outcome == "Too Low"
 
def test_check_guess_hint_direction_not_reversed():
    # This was the original Module 1 bug — verifies the fix holds
    outcome, msg = check_guess(80, 40)
    assert outcome == "Too High"
    assert "LOWER" in msg
 
 
# ── parse_guess ────────────────────────────────────────────────────────────────
 
def test_parse_guess_valid():
    ok, val, err = parse_guess("42", 1, 100)
    assert ok is True
    assert val == 42
    assert err is None
 
def test_parse_guess_empty_string():
    ok, val, err = parse_guess("", 1, 100)
    assert ok is False
    assert "guess" in err.lower()
 
def test_parse_guess_none():
    ok, val, err = parse_guess(None, 1, 100)
    assert ok is False
 
def test_parse_guess_not_a_number():
    ok, val, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert "number" in err.lower()
 
def test_parse_guess_out_of_range_high():
    ok, val, err = parse_guess("200", 1, 100)
    assert ok is False
    assert "between" in err.lower()
 
def test_parse_guess_out_of_range_low():
    ok, val, err = parse_guess("0", 1, 100)
    assert ok is False
 
def test_parse_guess_decimal_rounds():
    ok, val, err = parse_guess("7.9", 1, 100)
    assert ok is True
    assert val == 7
 
def test_parse_guess_exact_low_boundary():
    ok, val, err = parse_guess("1", 1, 100)
    assert ok is True
    assert val == 1
 
def test_parse_guess_exact_high_boundary():
    ok, val, err = parse_guess("100", 1, 100)
    assert ok is True
    assert val == 100
 
 
# ── update_score ───────────────────────────────────────────────────────────────
 
def test_update_score_win_early():
    # Win on attempt 1: 100 - 10*(1+1) = 80
    score = update_score(0, "Win", 1)
    assert score == 80
 
def test_update_score_win_never_below_10():
    # Win very late — floor at 10
    score = update_score(0, "Win", 20)
    assert score == 10
 
def test_update_score_win_adds_to_existing():
    score = update_score(50, "Win", 1)
    assert score == 130
 
def test_update_score_too_low_decreases():
    score = update_score(20, "Too Low", 3)
    assert score == 15
 
def test_update_score_too_high_even_attempt_bonus():
    score = update_score(20, "Too High", 2)
    assert score == 25
 
def test_update_score_too_high_odd_attempt_penalty():
    score = update_score(20, "Too High", 3)
    assert score == 15
 
def test_update_score_unknown_outcome_no_change():
    score = update_score(30, "Draw", 1)
    assert score == 30
 
 
# ── get_range_for_difficulty ───────────────────────────────────────────────────
 
def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)
 
def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)
 
def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)
 
def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)