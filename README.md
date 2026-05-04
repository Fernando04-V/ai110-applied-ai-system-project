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
 
# Design Decisions
 
## Why a rule-based AI coach instead of a language model?
- 

## Why a Reliability/Testing System as the AI feature?
- 
 

---
 
# Testing Summary
 
Run with: `pytest -v`
 

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