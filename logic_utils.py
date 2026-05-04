"""
logic_utils.py
--------------
Core game logic for Glitchy Guesser.
Refactored from app.py during Module 1 debugging project.
All three original bugs were fixed here:
  - Wrong hint direction (check_guess)
  - Out-of-range inputs accepted silently (parse_guess)
  - Score logic rewarding wrong guesses (update_score)
"""


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# FIX: Refactored parse_guess into logic_utils.py using AI assistance.
# Now rejects empty input, non-numbers, decimals, and out-of-range values.
def parse_guess(raw: str, low: int, high: int):
    """
    Parse and validate user input into an integer guess.

    Args:
        raw: the raw string from the text input
        low: minimum allowed value (inclusive)
        high: maximum allowed value (inclusive)

    Returns:
        (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."
    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Please enter a number between {low} and {high}."

    return True, value, None


# FIX: Refactored check_guess into logic_utils.py using AI assistance.
# Original bug: hint direction was inverted. Now correctly returns Too High / Too Low.
def check_guess(guess, secret):
    """
    Compare a guess to the secret number.

    Args:
        guess: the player's integer guess
        secret: the secret integer

    Returns:
        (outcome: str, message: str)
        outcome is one of: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "Correct!"
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == str(secret):
            return "Win", "Correct!"
        if g > str(secret):
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


# FIX: Refactored update_score into logic_utils.py using AI assistance.
# Original bug: rewarded wrong guesses unconditionally. Now only awards
# a small bonus on even-numbered attempts to add variation without being exploitable.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate the new score based on the outcome of a guess.

    Args:
        current_score: the player's current score
        outcome: "Win", "Too High", or "Too Low"
        attempt_number: which attempt this was (1-indexed)

    Returns:
        Updated integer score
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score