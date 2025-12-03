import streamlit as st
import numpy as np

st.title("🟩 Blockade / Snake-Style Game")

# --- Settings ---
GRID_SIZE = 20

# --- Initialize session state ---
if "pos" not in st.session_state:
    st.session_state.pos = [GRID_SIZE // 2, GRID_SIZE // 2]  # snake head
    st.session_state.trail = set()
    st.session_state.game_over = False

# --- Direction buttons ---
st.write("Use the buttons to move:")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Left"):
        move = (-1, 0)
    else:
        move = None
with col2:
    if st.button("⬆️ Up"):
        move = (0, -1)
with col3:
    if st.button("⬇️ Down"):
        move = (0, 1)

if st.button("➡️ Right"):
    move = (1, 0)

# --- Move handler ---
if move and not st.session_state.game_over:
    x, y = st.session_state.pos
    dx, dy = move
    new_pos = [x + dx, y + dy]

    # Check out of bounds
    if (
        new_pos[0] < 0 or new_pos[0] >= GRID_SIZE or
        new_pos[1] < 0 or new_pos[1] >= GRID_SIZE
    ):
        st.session_state.game_over = True

    # Check collision with trail
    elif tuple(new_pos) in st.session_state.trail:
        st.session_state.game_over = True
    else:
        # Leave a trail where we were
        st.session_state.trail.add(tuple(st.session_state.pos))
        st.session_state.pos = new_pos

# --- Render board ---
board = np.full((GRID_SIZE, GRID_SIZE), "⬜")

# Draw trail
for t in st.session_state.trail:
    board[t[1]][t[0]] = "🟦"

# Draw head
x, y = st.session_state.pos
board[y][x] = "🟩"

# Show board
board_str = "\n".join("".join(row) for row in board)
st.markdown(f"<pre style='font-size:20px'>{board_str}</pre>", unsafe_allow_html=True)

# --- Game Over ---
if st.session_state.game_over:
    st.error("💥 Game Over! You hit a wall or your own trail.")
    if st.button("Restart"):
        st.session_state.pos = [GRID_SIZE // 2, GRID_SIZE // 2]
        st.session_state.trail = set()
        st.session_state.game_over = False
