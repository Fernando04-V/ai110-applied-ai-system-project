# Applied AI System: Glitchy Guesser + AI Reliability Coach
 
## Original Project
 
- This project extends **Game Glitch Investigator** from Module 1 of AI110. The original project was a Streamlit number-guessing game intentionally filled with bugs such as wrong hints, resetting secret numbers, and broken scoring. The goal was to identify, document, and fix those bugs using AI-assisted debugging tools like GitHub Copilot. Core logic was refactored from `app.py` into `logic_utils.py`, and automated tests were added using `pytest`.
 
---
 
## Summary
- This project extends the module 1 project by adding an AI coach extension where it helps guide the player towards a more systematic approach towars guessing the correct number.
I made this extension because in these sorts of games, players often just guess at random rather than attempting to play with a strategy. Adding an AI coach that aids the player rather than giving the answer i think reflects on our use with AI. The use should be that AI serves as a tool, not as something that does everything for us which takes out the learning curve or in this case the fun!
 
---
 
## [ Architecture Overview ](assets/systemDiagram.png)
 
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
   ```
   Run from root: 
      pytest tests/test_game_logic.py -v
      pytest tests/test_evaluator.py -v
   ```
 
---
 
## Sample Interactions
 
**Example 1 — Correct guess with hint:**
- Difficulty: Normal (range 1–100)
- Input: `23` (secret is 48)
- Output: `📈 Go HIGHER!`
- Log: `2026-05-03 19:05:18,346 | INFO | Guess submitted | guess=23 | secret=48 | outcome=Too Low | attempt=1`

**Example 2 — Invalid input caught by guardrail:**
- Input: `111` (out of range)
- Output: `Please enter a number between 1 and 100.`
- Log: `2026-05-03 19:06:54,863 | INFO | Invalid guess | raw='1111' | error=Please enter a number between 1 and 100.`

**Example 3 — AI coach detects random guessing:**
- Guess history: `[23, 78, 50]`
- Coach output: `Your guesses look a bit random. Try a more systematic approach — guess 64 to cut the remaining range in half.`
- Strategy Score: `3.35 pts (Moderate)`
- log: `2026-05-03 20:49:12,827 | INFO | AI tip requested | history=[(23, 'Too Low'), (78, 'Too High'), (50, 'Too Low')] | confidence=0.67`

**Example 4 — AI coach detects binary search with secret number less than 75 :**
- Guess history: `[50, 75, 62]`
- Coach output: `💡 Solid binary search strategy! You're narrowing it down efficiently. Your next best guess is around 68.`
- Strategy Score: `3.30 pts (Moderate)`

**Example 5 — Win:**
- Input: `63`
- Output: Balloons 🎈 + `You won! The secret was 63. Final score: 80`
- Log: `2026-05-03 20:48:31,336 | INFO | Game WON | attempts=1 | score=80`

---
 
# Design Decisions

 
## Why a rule-based AI coach instead of a language model?
- I went with a ruled-based reasoning system because of its deterministic nature and because i requires no API Key to work with. 
After finishing unit 7, i was inspired to continue working with a system that followed a "points system" path.I specially found this fitting to the problem i attempted to address
which was to analyze a user's inputs and do something productive with it

## Trade-Offs
- Choose a rule-based system rather than a LLM as it does not require an API key. However, the catch is that the same system only recognizes fixed patters like binary search
- Wen with (guess, outcome) tuples rather than plain integer history as it allows evaluate_confident to accurately track the shriinking window. However, it mae the data strucutre more comple and required more additions in the app.py

---
 
# Testing Summary: What worked, what didn't, and what you learned.

## What Worked
- All tests from both test files passed which means that the behaviour of the programs went as expected.
- The test test_check_guess_hint_direction_not_reserved served as a regression guard for the first module reversed hint bug. THis test passed well which cofirmed that the fix held 

## What Didnt' Work
- At first the evaluate_confidence had no score floor
- The test test_confident_equal_range_returns_1 caught a potential divide by zero when high equaled low. 

## What I Learned
- Making edge cases poitned out bugs that normal gameplay would rarely trigger.
- The evaluate_confident bug was invisible during manual testing becaseu typical guesses dont yield exact cancellation as only as targeted test revealed it


---
 
# Reflection and Ethics
 
## What are the limitation or biases in your system?
- The strategy scorer only rewards one strategy, binary search. A player using a valid but different approach, like guessing one above the last "too low," would be labeled as random
 
## Could your AI be misued, and how woud you prevent that?
- A player could artificially inflate their Strategy Score by always guessing near midpoints regardless of game feedback, optimizing for the score rather than the game. Since the score is cosmetic, it's low stakes, but the debug expander already exposes the secret number, which is a more direct exploit worth removing in production.
 
## What suprised you while testing your AI's reliability?
- There was a time during testing that having a guessing sequence like 50 and 75 it would yield exactly 0.0 because a negative per-guess score cancelled out the previous score. In other words, testing pointed out that the formula had no floor.

## Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.
- It was both helpful but t the same time flawed. Helpful in the sense that AI helped me in identifying the window-narrowing logic in evaluate_confidence which was fundamentally broken without outcome data and proposed (guess, outcome) tuples throughout the history of guesses.
Flawed in the sense that in the original evaluate_confidence design returned a score between 0.0 to 1.0 but had no clamp which caused scores going negative and yield imsleading results.

## What this project says about me as an AI engineer?
- 

---
 
# [ Video Walkthrough ](assets/ai110_demo.mp4)
 
---
 
# Porfolio Artifact

## Github Link: https://github.com/Fernando04-V/ai110-applied-ai-system-project.git