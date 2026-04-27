import json
import requests
import os

"""
evaluator.py
------------
AI-powered hint evaluator. Uses the Claude API to analyze a player's
guess history and return a strategic suggestion.
"""



CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"


def evaluate_guess_history(history: list, secret_range: tuple, attempt_limit: int) -> str:
    """
    Send the player's guess history to Claude and get a strategic tip back.

    Args:
        history: list of integer guesses made so far
        secret_range: (low, high) tuple of the game range
        attempt_limit: max attempts allowed in this game

    Returns:
        A short strategic tip string from Claude, or a fallback message on error.
    """
    if not history:
        return "No guesses yet — try starting with the middle of the range!"

    low, high = secret_range
    attempts_used = len(history)
    attempts_remaining = attempt_limit - attempts_used

    prompt = f"""You are a coach for a number guessing game. The player is guessing a secret number between {low} and {high}.
They have {attempts_remaining} attempts remaining out of {attempt_limit} total.
Their guesses so far (in order) were: {history}.

Analyze their guessing pattern in 1-2 short sentences. 
Tell them if they are being strategic (e.g. using binary search) or random. 
Give one concrete tip for their next guess. Be encouraging but direct.
Do NOT reveal the secret number. Keep your response under 40 words."""

    try:
        response = requests.post(
        CLAUDE_API_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": MODEL,
            "max_tokens": 100,
            "messages": [{"role": "user", "content": prompt}],
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data["content"][0]["text"].strip()

    except requests.exceptions.Timeout:
        return "⚠️ AI coach timed out. Try guessing the midpoint of your remaining range!"
    except requests.exceptions.RequestException as e:
        return f"⚠️ AI coach unavailable: {str(e)}"
    except (KeyError, IndexError):
        return "⚠️ Unexpected response from AI coach. Keep going — you've got this!"


def evaluate_confidence(history: list, secret_range: tuple) -> float:
    """
    Calculate a simple confidence score (0.0 - 1.0) based on how
    strategically the player is narrowing the range.

    A player doing perfect binary search scores ~1.0.
    A player guessing randomly scores closer to 0.0.

    Args:
        history: list of integer guesses
        secret_range: (low, high) tuple

    Returns:
        Float between 0.0 and 1.0
    """
    if len(history) < 2:
        return 0.5  # Not enough data

    low, high = secret_range
    total_range = high - low
    if total_range == 0:
        return 1.0

    # Measure how much range each guess eliminated
    elimination_scores = []
    current_low, current_high = low, high

    for guess in history:
        if not isinstance(guess, int):
            continue
        midpoint = (current_low + current_high) / 2
        distance_from_mid = abs(guess - midpoint)
        max_distance = (current_high - current_low) / 2
        if max_distance == 0:
            score = 1.0
        else:
            # Closer to midpoint = better binary search = higher score
            score = 1.0 - (distance_from_mid / max_distance)
        elimination_scores.append(score)

        # Update theoretical range based on guess direction
        if guess < midpoint:
            current_low = guess
        else:
            current_high = guess

    if not elimination_scores:
        return 0.5

    return round(sum(elimination_scores) / len(elimination_scores), 2)