import streamlit as st
import pandas as pd
import copy

def is_valid(grid, r, c, k):
    for i in range(9):
        if grid[r][i] == k: return False
        if grid[i][c] == k: return False
    box_r = r // 3 * 3
    box_c = c // 3 * 3
    for i in range(3):
        for j in range(3):
            if grid[box_r + i][box_c + j] == k: return False
    return True

def solve_sudoku(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for k in range(1, 10):
                    if is_valid(grid, r, c, k):
                        grid[r][c] = k
                        if solve_sudoku(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True

def check_solution(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return False, "Incomplete. Keep trying!"
            if grid[r][c] < 1 or grid[r][c] > 9:
                return False, "Only numbers 1-9 are allowed!"
                
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            grid[r][c] = 0
            if not is_valid(grid, r, c, val):
                grid[r][c] = val
                return False, "Try again. Constraints violated!"
            grid[r][c] = val
    return True, "You won!"

st.set_page_config(page_title="Sudoku Solver", layout="centered", page_icon="🧩")

# Clean, neat, professional CSS
st.markdown("""
<style>
    /* Clean layout resets */
    div[data-testid="column"] {
        padding: 0 !important;
    }
    div[data-testid="stVerticalBlock"] > div > div {
        gap: 0 !important;
    }
    
    /* Neatly styled text inputs */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    div[data-testid="stTextInput"] input {
        width: 100% !important;
        height: 50px !important;
        font-size: 22px !important;
        font-weight: 500 !important;
        text-align: center !important;
        border-radius: 0 !important;
        border: 1px solid #444 !important;
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        margin: 0 !important;
        padding: 0 !important;
        transition: background-color 0.2s ease;
    }
    div[data-testid="stTextInput"] input:focus {
        background-color: #3b4252 !important;
        border-color: #88c0d0 !important;
        color: #eceff4 !important;
    }
    
    /* Board wrapper for a neat border */
    .board-wrapper {
        border: 4px solid #555;
        padding: 2px;
        background-color: #111;
        width: 100%;
        max-width: 450px;
        margin: 0 auto;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    /* Titles and buttons */
    h1 {
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #eceff4;
        font-weight: 600;
        margin-bottom: 5px !important;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 25px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧩 Sudoku Solver")
st.markdown("<div class='subtitle'>A clean, interactive Constraint Satisfaction Problem tool.</div>", unsafe_allow_html=True)

initial_puzzle = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if 'puzzle' not in st.session_state:
    st.session_state.puzzle = copy.deepcopy(initial_puzzle)

def update_puzzle_from_cells():
    for r in range(9):
        for c in range(9):
            val = st.session_state.get(f"cell_{r}_{c}", "")
            if val.isdigit() and 1 <= int(val) <= 9:
                st.session_state.puzzle[r][c] = int(val)
            else:
                st.session_state.puzzle[r][c] = 0

# A small trick to center the board: use empty columns on sides
spacer1, board_col, spacer2 = st.columns([1, 4, 1])

with board_col:
    st.markdown("<div class='board-wrapper'>", unsafe_allow_html=True)
    for r in range(9):
        cols = st.columns(9)
        for c in range(9):
            val = st.session_state.puzzle[r][c]
            val_str = str(val) if val != 0 else ""
            with cols[c]:
                st.text_input(
                    label=f"hidden_{r}_{c}",
                    value=val_str,
                    key=f"cell_{r}_{c}",
                    max_chars=1,
                    on_change=update_puzzle_from_cells
                )
        # Add slight vertical spacing to mimic 3x3 blocks
        if r in [2, 5]:
            st.markdown("<div style='height: 4px; background-color: #555;'></div>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("✅ Check Solution", use_container_width=True):
        update_puzzle_from_cells()
        is_won, msg = check_solution(st.session_state.puzzle)
        if is_won:
            st.success(msg)
            st.balloons()
        else:
            st.error(msg)

with c2:
    if st.button("🤖 Auto Solve", use_container_width=True):
        grid_copy = copy.deepcopy(initial_puzzle)
        if solve_sudoku(grid_copy):
            st.session_state.puzzle = grid_copy
            st.rerun()
        else:
            st.error("No solution exists!")

with c3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.puzzle = copy.deepcopy(initial_puzzle)
        st.rerun()
