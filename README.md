# 🤖 AI Problem Solving Assignment

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Machine Learning](https://img.shields.io/badge/Machine_Learning-scikit--learn-orange.svg)
![CSP](https://img.shields.io/badge/Algorithm-CSP_Backtracking-brightgreen.svg)

This repository contains professional, interactive solutions for two Artificial Intelligence problems using **Streamlit**. 

> 🌐 **Live Demo Status**: You can deploy these apps instantly for free using [Streamlit Community Cloud](https://share.streamlit.io/) by linking this GitHub repository!

---

## 🧩 Problem 6: Sudoku Solver (Constraint Satisfaction Problem)

### Overview
An interactive 9x9 Sudoku solver that utilizes the **Constraint Satisfaction Problem (CSP)** approach with a backtracking algorithm. The user can play manually or let the AI solve it instantly.

### 📸 Screenshots
**Input State (Manual Play)**
![Sudoku Input](assets/sudoku_input.png)

**Output State (AI Solved)**
![Sudoku Output](assets/sudoku_output.png)

### Execution Steps
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📈 Problem 18: Student Performance Predictor

### Overview
A Machine Learning web application using a **Random Forest Regressor** to predict final exam scores based on hours studied, attendance, prior scores, and assignments completed. Features real-time interactive data editing that instantly retrains the AI model.

### 📸 Screenshots
**Data Editor & Model Training (Input)**
![Predictor Input](assets/predictor_input.png)

**Prediction Form (Output)**
![Predictor Output](assets/predictor_output.png)

### Execution Steps
```bash
pip install -r requirements.txt
streamlit run app.py
```
