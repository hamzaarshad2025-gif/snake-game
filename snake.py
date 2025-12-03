import streamlit as st
import numpy as np
import random

st.title("🟦 Simple Tetris (Streamlit Turn-Based)")

ROWS, COLS = 20, 10

# Tetromino shapes
SHAPES = {
    "I": [[1,1,1,1]],
    "O": [[1,1],[1,1]],
    "T": [[1,1,1],[0,1,0]],
    "L": [[1,1,1],[1,0,0]],
    "J": [[1,1,1],[0,0,1]],
    "S": [[0,1,1],[1,1,0]],
    "Z": [[1,1,0],[0,1,1]]
}

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

# --- Initialize Session State ---
if "board" not in st.session_state:
    st.session_state.board = np.zeros((ROWS, COLS), dtype=int)
    st.session_state.shape = random.choice(list(SHAPES.keys()))
    st.session_state.block = SHAPES[st.session_state.shape]
    st.session_state.x = 3
    st.session_state.y = 0
    st.session_state.game_over = False
    st.session_state.score = 0

def collision(block, x, y):
    for r, row in enumerate(block):
        for c, val in enumerate(row):
            if val:
                if (y+r >= ROWS or 
                    x+c < 0 or 
                    x+c >= COLS or 
                    st.session_state.board[y+r][x+c]):
                    return True
    return False

def place_block():
    for r, row in enumerate(st.session_state.block):
        for c, val in enumerate(row):
            if val:
                st.session_state.board[st.session_state.y+r][st.session_state.x+c] = 1

def spawn_new():
    st.session_state.shape = random.choice(list(SHAPES.keys()))
    st.session_state.block = SHAPES[st.session_state.shape]
    st.session_state.x = 3
    st.session_state.y = 0
    if collision(st.session_state.block, 3, 0):
        st.session_state.game_over = True

def clear_lines():
    board = st.session_state.board
    new = [row for row in board if not all(row)]
    cleared = ROWS - len(new)
    if cleared > 0:
        st.session_state.score += cleared * 100
        new = [np.zeros(COLS, dtype=int)] * cleared + new
    st.session_state.board = np.array(new)

# --- Controls ---
col1, col2, col3, col4 = st.columns(4)
left = col1.button("⬅ Left")
right = col2.button("➡ Right")
rot = col3.button("🔄 Rotate")
down = col4.button("⬇ Step Down")

if not st.session_state.game_over:
    bx, by = st.session_state.x, st.session_state.y
    block = st.session_state.block

    # Process buttons
    if left and not collision(block, bx - 1, by):
        st.session_state.x -= 1
    if right and not collision(block, bx + 1, by):
        st.session_state.x += 1
    if rot:
        new_block = rotate(block)
        if not collision(new_block, bx, by):
            st.session_state.block = new_block
    if down:
        by += 1
        if not collision(block, bx, by):
            st.session_state.y = by
        else:
            place_block()
            clear_lines()
            spawn_new()

# --- Render the game board ---
display = st.session_state.board.copy()

# draw falling block
if not st.session_state.game_over:
    for r, row in enumerate(st.session_state.block):
        for c, val in enumerate(row):
            if val:
                display[st.session_state.y+r][st.session_state.x+c] = 2

# Convert to emoji board
emoji = {0: "⬛", 1: "🟩", 2: "🟦"}  # background, locked block, falling block
board_str = "\n".join("".join(emoji[val] for val in row) for row in display)

st.markdown(f"<pre style='font-size:18px; line-height:18px'>{board_str}</pre>", unsafe_allow_html=True)

st.write(f"**Score:** {st.session_state.score}")

# Restart Option
if st.session_state.game_over:
    st.error("💥 Game Over!")
    if st.button("Restart"):
        st.session_state.board = np.zeros((ROWS, COLS), dtype=int)
        st.session_state.score = 0
        st.session_state.game_over = False
        spawn_new()

