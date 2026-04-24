import streamlit as st

st.set_page_config(
    page_title="AI Problem Solving Assignment",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Problem Solving Assignment")
st.markdown("---")

st.markdown("""
### Welcome to the assignment portal!

Please use the **sidebar navigation on the left** to switch between the two different applications:

- **🧩 Problem 6: Sudoku Solver**  
  An interactive, premium-designed Sudoku grid that uses the Constraint Satisfaction Problem (CSP) backtracking algorithm to automatically solve puzzles.

- **📈 Problem 18: Student Predictor**  
  A Machine Learning application that uses a Random Forest Regressor to predict student exam scores based on hours studied and attendance.

👈 **Click the links in the sidebar to get started!**
""")
