import streamlit as st
import pandas as pd
import copy

def is_valid(grid, r, c, k):
    # Check row
    for i in range(9):
        if grid[r][i] == k: return False
    # Check column
    for i in range(9):
        if grid[i][c] == k: return False
    # Check 3x3 box
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
    # Check if there are any empty cells
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return False, "Incomplete. Keep trying!"
            if grid[r][c] < 1 or grid[r][c] > 9:
                return False, "Only numbers 1-9 are allowed!"
                
    # Check validity
    for r in range(9):
        for c in range(9):
            val = grid[r][c]
            grid[r][c] = 0 # temporarily remove
            if not is_valid(grid, r, c, val):
                grid[r][c] = val
                return False, "Try again. Constraints violated!"
            grid[r][c] = val
    return True, "You won!"

st.set_page_config(page_title="Prime Sudoku", layout="centered", page_icon="🧩")

# === PREMIUM CSS INJECTION ===
st.markdown("""
<style>
    /* Global Background and Fonts */
    .stApp {
        background: radial-gradient(circle at top, #1a0000, #000000);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Styling */
    h1 {
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #FF2B2B, #ff7b00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(255, 43, 43, 0.4);
        margin-bottom: 2rem !important;
    }

    /* Target the container of text inputs */
    div[data-testid="stVerticalBlock"] {
        gap: 0.2rem !important;
    }
    div[data-testid="column"] {
        padding: 0 !important;
        display: flex;
        justify-content: center;
    }
    
    /* Style the Text Inputs to look like Sudoku cells */
    div[data-testid="stTextInput"] {
        width: 100%;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="stTextInput"] label {
        display: none !important; /* Hide labels */
    }
    div[data-testid="stTextInput"] input {
        width: 45px !important;
        height: 45px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        text-align: center !important;
        border-radius: 8px !important;
        border: 2px solid rgba(255, 43, 43, 0.3) !important;
        background: rgba(20, 0, 0, 0.6) !important;
        color: #FF2B2B !important;
        box-shadow: inset 0 0 10px rgba(255,43,43,0.1);
        transition: all 0.3s ease !important;
        caret-color: transparent !important;
    }
    
    /* Hover & Focus Micro-Animations */
    div[data-testid="stTextInput"] input:hover {
        border-color: #FF2B2B !important;
        box-shadow: 0 0 15px rgba(255, 43, 43, 0.5), inset 0 0 10px rgba(255, 43, 43, 0.2);
        transform: scale(1.05);
        z-index: 10;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #ff7b00 !important;
        color: #ff7b00 !important;
        box-shadow: 0 0 20px rgba(255, 123, 0, 0.8), inset 0 0 15px rgba(255, 123, 0, 0.4) !important;
        transform: scale(1.1);
        z-index: 20;
    }

    /* Style the main container holding the grid to give it a glassmorphic card look */
    .sudoku-board {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        margin: 0 auto;
        max-width: 600px;
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #FF2B2B, #ff7b00) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(255, 43, 43, 0.4) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255, 43, 43, 0.6) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("PRIME SUDOKU")

st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem; margin-bottom: 2rem;'>The Ultimate Constraint Satisfaction Engine</p>", unsafe_allow_html=True)

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

def update_cells_from_puzzle():
    for r in range(9):
        for c in range(9):
            val = st.session_state.puzzle[r][c]
            st.session_state[f"cell_{r}_{c}"] = str(val) if val != 0 else ""

def update_puzzle_from_cells():
    for r in range(9):
        for c in range(9):
            val = st.session_state.get(f"cell_{r}_{c}", "")
            if val.isdigit() and 1 <= int(val) <= 9:
                st.session_state.puzzle[r][c] = int(val)
            else:
                st.session_state.puzzle[r][c] = 0

# Initialize session state cells if not present
if "cell_0_0" not in st.session_state:
    update_cells_from_puzzle()

st.markdown('<div class="sudoku-board">', unsafe_allow_html=True)

# Render the 9x9 grid
for r in range(9):
    cols = st.columns(9)
    for c in range(9):
        with cols[c]:
            st.text_input(
                label=f"r{r}c{c}", 
                key=f"cell_{r}_{c}", 
                max_chars=1,
                on_change=update_puzzle_from_cells # Sync state on every keypress
            )
            
st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.write("")

# Action Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Validate Board", use_container_width=True):
        update_puzzle_from_cells()
        is_won, msg = check_solution(st.session_state.puzzle)
        if is_won:
            st.success(msg)
            st.balloons()
        else:
            st.error(msg)

with col2:
    if st.button("🤖 Prime Auto-Solve", use_container_width=True):
        grid_copy = copy.deepcopy(initial_puzzle)
        if solve_sudoku(grid_copy):
            st.session_state.puzzle = grid_copy
            update_cells_from_puzzle()
            st.rerun()
        else:
            st.error("Algorithm failed. No solution exists!")

with col3:
    if st.button("🔄 System Reset", use_container_width=True):
        st.session_state.puzzle = copy.deepcopy(initial_puzzle)
        update_cells_from_puzzle()
        st.rerun()
