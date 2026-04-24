import streamlit as st
import pandas as pd
import copy

def is_valid(grid, r, c, k):
    for i in range(9):
        if grid[r][i] == k: return False
    for i in range(9):
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
st.title("🧩 Sudoku Solver (CSP)")

st.markdown("""
**How to play:**
- Fill in the missing numbers (1-9) in the grid.
- Click **Check Solution** to evaluate your answer.
- Click **Auto Solve (CSP)** to let the AI solve it.
""")

if 'initial_puzzle' not in st.session_state:
    st.session_state.initial_puzzle = [
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
    st.session_state.current_puzzle = copy.deepcopy(st.session_state.initial_puzzle)

def reset_puzzle():
    st.session_state.current_puzzle = copy.deepcopy(st.session_state.initial_puzzle)

df = pd.DataFrame(st.session_state.current_puzzle)
df = df.replace(0, None)
df.columns = [str(i) for i in range(1, 10)]

edited_df = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    key="data_editor"
)

try:
    current_grid = edited_df.fillna(0).astype(int).values.tolist()
except ValueError:
    st.error("Please enter only valid integers.")
    current_grid = copy.deepcopy(st.session_state.current_puzzle)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ Check Solution", use_container_width=True):
        is_won, msg = check_solution(current_grid)
        if is_won:
            st.success(msg)
            st.balloons()
        else:
            st.error(msg)

with col2:
    if st.button("🤖 Auto Solve (CSP)", use_container_width=True):
        grid_copy = copy.deepcopy(st.session_state.initial_puzzle)
        if solve_sudoku(grid_copy):
            st.session_state.current_puzzle = grid_copy
            st.rerun()
        else:
            st.error("No solution exists!")

with col3:
    if st.button("🔄 Reset Grid", use_container_width=True):
        reset_puzzle()
        st.rerun()
