"""
app.py
------
Glitchy Guesser — extended with AI coaching, confidence scoring, and game logging.
Original Module 1 project extended for the Applied AI System final project.
"""

import random
import logging
import streamlit as st
from logic_utils import check_guess, update_score, parse_guess
from evaluator import evaluate_guess_history, evaluate_confidence

# ── Logging setup ──────────────────────────────────────────────────────────────
logging.basicConfig(
    filename="game_log.txt",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_event(event: str):
    """Log a game event to game_log.txt."""
    logging.info(event)


# ── Difficulty helpers ─────────────────────────────────────────────────────────
def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game — now with an AI reliability coach.")

# ── Sidebar settings ───────────────────────────────────────────────────────────
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# ── Session state init ─────────────────────────────────────────────────────────
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
    log_event(f"New game started | difficulty={difficulty} | secret={st.session_state.secret}")

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "ai_tip" not in st.session_state:
    st.session_state.ai_tip = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None

# ── Main UI ────────────────────────────────────────────────────────────────────
st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts + 1}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# ── AI Coach section ───────────────────────────────────────────────────────────
st.divider()
st.subheader("🤖 AI Coach")
ask_ai = st.button("Get AI Strategy Tip")

if ask_ai:
    int_history = [g for g in st.session_state.history if isinstance(g, int)]
    with st.spinner("Asking AI coach..."):
        tip = evaluate_guess_history(int_history, (low, high), attempt_limit)
        confidence = evaluate_confidence(int_history, (low, high))
    st.session_state.ai_tip = tip
    st.session_state.confidence = confidence
    log_event(f"AI tip requested | history={int_history} | confidence={confidence}")

if st.session_state.ai_tip:
    st.info(f"💡 {st.session_state.ai_tip}")

if st.session_state.confidence is not None:
    conf = st.session_state.confidence
    label = "🟢 Strategic" if conf >= 0.7 else ("🟡 Moderate" if conf >= 0.4 else "🔴 Random")
    st.metric("Strategy Score", f"{conf:.0%}", label)

# ── New Game ───────────────────────────────────────────────────────────────────
#FIX: Refactored this part of the code with Claude to allow users to start a new game at any given time
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.ai_tip = None
    st.session_state.confidence = None
    log_event(f"Game reset | difficulty={difficulty} | new secret={st.session_state.secret}")
    st.success("New game started.")
    st.rerun()

# ── Guard: already won/lost ────────────────────────────────────────────────────
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# ── Submit guess ───────────────────────────────────────────────────────────────
if submit:
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
        log_event(f"Invalid guess | raw='{raw_guess}' | error={err}")
    else:
        st.session_state.history.append(guess_int)
        outcome, message = check_guess(guess_int, st.session_state.secret)
        log_event(
            f"Guess submitted | guess={guess_int} | secret={st.session_state.secret} "
            f"| outcome={outcome} | attempt={st.session_state.attempts}"
        )

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            log_event(
                f"Game WON | attempts={st.session_state.attempts} | score={st.session_state.score}"
            )
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                log_event(
                    f"Game LOST | secret={st.session_state.secret} | score={st.session_state.score}"
                )
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")