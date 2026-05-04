# Applied AI System: Glitchy Guesser + AI Reliability Coach
 
## Original Project
 
This project extends **Game Glitch Investigator** from Module 1 of AI110.
 
The original project was a Streamlit number-guessing game intentionally filled with bugs — wrong hints, resetting secret numbers, and broken scoring. The goal was to identify, document, and fix those bugs using AI-assisted debugging tools like GitHub Copilot. Core logic was refactored from `app.py` into `logic_utils.py`, and automated tests were added using `pytest`.
 
---
 
## Summary
 
This extended system adds a **rule-based AI Reliability Coach** on top of the repaired guessing game. Players can request strategic tips mid-game based on their guess history, receive a **strategy confidence score** that rates how efficiently they are narrowing the range, and every guess is automatically logged to a local file for traceability.
 
The AI coach uses rule-based reasoning — a classical form of AI — to observe the player's guess history, detect their strategy pattern (binary search, random guessing, tiny steps, repeated guesses), and return a personalized tip with a concrete next number to try. No external API or internet connection is required.
 
The goal is to demonstrate a complete applied AI system: a working application, an integrated AI feature, automated testing, and clear logging and guardrails.
 
---
 
## [Architecture Overview] (assets/systemDiagram.png)
 
---
 
## Setup Instructions
 
**Prerequisites:** Python 3.10+
 
1. Clone the repository:
   ```bash
   git clone https://github.com/Fernando04-V/ai110-applied-ai-system-project.git
   cd applied-ai-system-project
   ```
 
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
 
3. Run the app:
   ```bash
   python -m streamlit run app.py
   ```
 
4. Run the test suite:
   ```bash
   pytest -v
   ```
 
---
 
## Sample Interactions
 
**Example 1 — Correct guess with hint:**
- Difficulty: Normal (range 1–100)
- Input: `50` (secret is 72)
- Output: `📈 Go HIGHER!`
- Log: `Guess submitted | guess=50 | secret=72 | outcome=Too Low | attempt=1`
**Example 2 — Invalid input caught by guardrail:**
- Input: `500` (out of range)
- Output: `Please enter a number between 1 and 100.`
- Log: `Invalid guess | raw='500' | error=Please enter a number between 1 and 100.`
**Example 3 — AI coach detects random guessing:**
- Guess history: `[15, 90, 22]`
- Coach output: `💡 Your guesses look a bit random. Try a more systematic approach — guess 50 to cut the remaining range in half.`
- Strategy Score: `20% 🔴 Random`
**Example 4 — AI coach detects binary search:**
- Guess history: `[50, 75, 62]`
- Coach output: `💡 Solid binary search strategy! You're narrowing it down efficiently. Your next best guess is around 68.`
- Strategy Score: `85% 🟢 Strategic`
**Example 5 — Win:**
- Input: `72`
- Output: Balloons 🎈 + `You won! The secret was 72. Final score: 60`
- Log: `Game WON | attempts=4 | score=60`
---
 
## Design Decisions
 
**Why a rule-based AI coach instead of a language model?**
A rule-based reasoning system was chosen because it is transparent, fully testable, deterministic, and requires no API key or internet connection. Every decision the coach makes can be traced to a specific line of code, which makes it more reliable and easier to evaluate than a black-box model call. This also means the coach works instantly with no latency or cost.
 
**Why a Reliability/Testing System as the AI feature?**
It was the most natural extension of a debugging-focused project. The original Module 1 was literally about fixing unreliable AI-generated code — adding a system that measures and improves reliability is a direct evolution of that theme.
 
**How the AI coach thinks:**
The coach receives the guess history and runs it through a prioritized set of pattern detection rules in order:
1. Empty history → suggest starting at the midpoint
2. Single guess → evaluate if it was near the ideal starting point
3. Repeated guesses → warn the player
4. Tiny steps → tell them to jump further
5. Low attempts remaining → give urgent best guess
6. Binary search detected → confirm and continue
7. Default → random pattern detected, suggest midpoint
**Tradeoffs:**
- The confidence score is a heuristic based on midpoint distance, not a true measure of optimal play. A player using a different valid strategy may score lower than expected.
- The coach does not receive the Too High / Too Low feedback from the game — it only sees the guess numbers. This means its suggested midpoint can occasionally fall outside the true remaining range. A future improvement would be passing hint outcomes alongside the guess history.
- Logging goes to a local flat file (`game_log.txt`) rather than a database. Simple and readable but does not scale.
---
 
## Testing Summary
 
Run with: `pytest -v`
 
| Test File | Tests | Result |
|---|---|---|
| `test_game_logic.py` | 25 | ✅ All pass |
| `test_evaluator.py` | 12 | ✅ All pass |
 
**What was tested:**
- `check_guess` covers win, too high, too low, and boundary cases
- `parse_guess` covers empty input, None, non-numeric, decimals, and out-of-range values
- `update_score` covers win (early and late), loss, and unknown outcomes
- `evaluate_confidence` covers no history, single guess, binary search, and random guesses
- `evaluate_guess_history` covers all pattern branches: empty history, single guess, repeated guesses, tiny steps, low attempts, binary search, and random guessing
**What was learned:**
- The `evaluate_confidence` function originally had a divide-by-zero bug when `max_distance` was 0 (equal range edges). A guard clause fixed this.
- Testing rule-based logic is straightforward because outputs are deterministic — the same inputs always produce the same output, so no mocking is needed.
---
 
## Reflection and Ethics
 
**Limitations and biases:**
The confidence score is biased toward binary search — a player using a different valid strategy (such as always guessing near boundaries) will score lower even if their logic is sound. The coach also works best with 3 or more guesses; with only 1 guess there is not enough pattern data to give specific advice.
 
**Misuse potential:**
The game is low-stakes. However, the pattern of observing and analyzing user behavior could be misused in a more sensitive application. Guardrails here include: the history contains only numbers with no personal information, the coach runs only on explicit user action, and all data stays local.
 
**Surprises during testing:**
The binary search detection worked well even with just 3 guesses. The hardest edge case was when the player guessed the exact midpoint on their first try — the coach needed a specific check to handle that gracefully rather than giving a generic tip.
 
**AI Collaboration:**
- **Helpful suggestion:** Claude suggested using the distance from the midpoint as a proxy for binary search quality when building `evaluate_confidence` — a clean heuristic that became the core of the scoring algorithm.
- **Flawed suggestion:** Claude initially suggested storing an API key directly in `app.py` as a hardcoded string. This is a security anti-pattern. The project was redesigned to use a fully local rule-based system instead, removing the need for any API key entirely.
---
 
## Video Walkthrough
 
[assets/ai110_demo.mp4]
 
---
 
## Portfolio Note
 
This project demonstrates my ability to take a broken AI-generated codebase, repair it thoughtfully, and extend it into a multi-component system with an integrated AI feature, automated testing, structured logging, and input guardrails. It reflects my approach to AI engineering: make it work, make it testable, make it explainable.