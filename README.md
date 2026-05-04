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
   ```bash
   pytest -v
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


 

---
 
# Testing
 
Run from root: 
- pytest tests/test_game_logic.py -v
- pytest tests/test_evaluator.py -v
 

---
 
# Reflection and Ethics
 
## What are the limitation or biases in your system?
- 
 
## Could your AI be misued, and how woud you prevent that?
- 
 
## What suprised you while testing your AI's reliability?
- 

## Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.
- 

---
 
# [ Video Walkthrough ](assets/ai110_demo.mp4)
 
---
 
# Porfolio Artifact

## Github Link: https://github.com/Fernando04-V/ai110-applied-ai-system-project.git

## What this project says about me as an AI engineer?
- 