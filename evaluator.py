"""
evaluator.py
------------
AI-powered hint evaluator. Analyzes a player's guess history and returns
a strategic suggestion using a rule-based reasoning system.
"""
 
 
def evaluate_guess_history(history: list, secret_range: tuple, attempt_limit: int) -> str:
    """
    Analyze the player's guess history and return a strategic coaching tip.
 
    Args:
        history: list of integer guesses made so far
        secret_range: (low, high) tuple of the game range
        attempt_limit: max attempts allowed in this game
 
    Returns:
        A short strategic tip string based on the player's pattern.
    """
    if not history:
        return "No guesses yet — try starting with the middle of the range!"
 
    int_history = [g for g in history if isinstance(g, int)]
 
    if not int_history:
        return "No valid guesses yet — make sure to enter a number!"
 
    low, high = secret_range
    attempts_remaining = attempt_limit - len(history)
    last_guess = int_history[-1]
    ideal_start = (low + high) // 2
 
    # Pattern: only one guess so far
    if len(int_history) == 1:
        distance_from_mid = abs(last_guess - ideal_start)
        range_size = high - low
        if distance_from_mid <= range_size * 0.1:
            return (
                f"Great start! Guessing near the middle ({ideal_start}) is the optimal "
                f"opening move. Keep splitting the remaining range in half."
            )
        else:
            return (
                f"Consider starting near {ideal_start} — the midpoint of {low}-{high}. "
                f"It cuts the range in half with every guess."
            )
 
    # Pattern: detect binary search behavior
    binary_search_count = 0
    current_low, current_high = low, high
    for guess in int_history:
        mid = (current_low + current_high) // 2
        if abs(guess - mid) <= (current_high - current_low) * 0.15:
            binary_search_count += 1
        if guess < mid:
            current_high = mid
        else:
            current_low = mid
 
    is_binary = binary_search_count >= len(int_history) * 0.6
 
    # Pattern: detect repeated guesses
    unique_guesses = len(set(int_history))
    if unique_guesses < len(int_history):
        return "You guessed the same number twice! Each guess should be different to eliminate possibilities."
 
    # Pattern: detect very small steps
    diffs = [abs(int_history[i] - int_history[i-1]) for i in range(1, len(int_history))]
    avg_step = sum(diffs) / len(diffs)
    range_size = high - low
    if avg_step < range_size * 0.05:
        next_mid = (current_low + current_high) // 2
        return (
            f"You're moving in very small steps — that could use up all your attempts. "
            f"Try jumping to {next_mid} to eliminate half the remaining range at once."
        )
 
    # Pattern: urgent warning if attempts running low
    if attempts_remaining <= 2:
        next_mid = (current_low + current_high) // 2
        return (
            f"Only {attempts_remaining} attempt(s) left — guess {next_mid} now. "
            f"It's the best chance to hit the target."
        )
 
    # Pattern: good binary search
    if is_binary:
        next_mid = (current_low + current_high) // 2
        return (
            f"Solid binary search strategy! You're narrowing it down efficiently. "
            f"Your next best guess is around {next_mid}."
        )
 
    # Pattern: random-looking guesses
    next_mid = (current_low + current_high) // 2
    return (
        f"Your guesses look a bit random. Try a more systematic approach — "
        f"guess {next_mid} to cut the remaining range in half."
    )
 
 
def evaluate_confidence(history: list, secret_range: tuple) -> float:
    """
    Calculate a confidence score (0.0 - 1.0) based on how strategically
    the player is narrowing the range using binary search.
 
    Args:
        history: list of integer guesses
        secret_range: (low, high) tuple
 
    Returns:
        Float between 0.0 and 1.0
    """
    if len(history) < 2:
        return 0.5
 
    low, high = secret_range
    total_range = high - low
    if total_range == 0:
        return 1.0
 
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
            score = 1.0 - (distance_from_mid / max_distance)
        elimination_scores.append(score)
 
        if guess < midpoint:
            current_high = midpoint
        else:
            current_low = midpoint
 
    if not elimination_scores:
        return 0.5
 
    return round(sum(elimination_scores) / len(elimination_scores), 2)
 