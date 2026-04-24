document.addEventListener('DOMContentLoaded', () => {
    const boardEl = document.getElementById('sudoku-board');
    const msgEl = document.getElementById('message-container');
    
    // Initial Puzzle (0 represents empty cells)
    const initialPuzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ];
    
    let currentGrid = [];
    const inputs = []; // Stores references to input elements

    // Initialize board
    function initBoard() {
        boardEl.innerHTML = '';
        currentGrid = JSON.parse(JSON.stringify(initialPuzzle)); // Deep copy
        
        for (let r = 0; r < 9; r++) {
            inputs[r] = [];
            for (let c = 0; c < 9; c++) {
                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'cell';
                input.maxLength = 1;
                
                if (initialPuzzle[r][c] !== 0) {
                    input.value = initialPuzzle[r][c];
                    input.readOnly = true;
                    input.classList.add('initial');
                }
                
                input.addEventListener('input', (e) => {
                    const val = e.target.value;
                    if (!/^[1-9]$/.test(val)) {
                        e.target.value = '';
                        currentGrid[r][c] = 0;
                    } else {
                        currentGrid[r][c] = parseInt(val);
                    }
                });
                
                boardEl.appendChild(input);
                inputs[r].push(input);
            }
        }
    }

    // Constraint Satisfaction Check
    function isValid(grid, r, c, k) {
        for (let i = 0; i < 9; i++) {
            if (grid[r][i] === k) return false;
            if (grid[i][c] === k) return false;
        }
        const boxR = Math.floor(r / 3) * 3;
        const boxC = Math.floor(c / 3) * 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (grid[boxR + i][boxC + j] === k) return false;
            }
        }
        return true;
    }

    // Backtracking Auto-Solver (CSP)
    function solveSudoku(grid) {
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                if (grid[r][c] === 0) {
                    for (let k = 1; k <= 9; k++) {
                        if (isValid(grid, r, c, k)) {
                            grid[r][c] = k;
                            if (solveSudoku(grid)) return true;
                            grid[r][c] = 0;
                        }
                    }
                    return false;
                }
            }
        }
        return true;
    }

    // Update UI from logic grid
    function updateUI() {
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                inputs[r][c].value = currentGrid[r][c] === 0 ? '' : currentGrid[r][c];
            }
        }
    }

    // Display Message
    function showMessage(msg, isSuccess) {
        msgEl.textContent = msg;
        msgEl.className = `message ${isSuccess ? 'success' : 'error'}`;
    }

    // Buttons
    document.getElementById('btn-validate').addEventListener('click', () => {
        // Check for empty
        let empty = false;
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                if (currentGrid[r][c] === 0) empty = true;
            }
        }
        if (empty) {
            showMessage("Incomplete. Keep trying!", false);
            return;
        }
        
        // Validate constraints
        let valid = true;
        for (let r = 0; r < 9; r++) {
            for (let c = 0; c < 9; c++) {
                const val = currentGrid[r][c];
                currentGrid[r][c] = 0; // Temp remove
                if (!isValid(currentGrid, r, c, val)) valid = false;
                currentGrid[r][c] = val; // Restore
            }
        }
        
        if (valid) {
            showMessage("You won! The board is completely valid.", true);
        } else {
            showMessage("Try again. Constraints violated!", false);
        }
    });

    document.getElementById('btn-solve').addEventListener('click', () => {
        // Reset to initial before solving to avoid unsolvable user states
        currentGrid = JSON.parse(JSON.stringify(initialPuzzle));
        if (solveSudoku(currentGrid)) {
            updateUI();
            showMessage("Solved automatically using CSP Backtracking!", true);
        } else {
            showMessage("No solution exists!", false);
        }
    });

    document.getElementById('btn-reset').addEventListener('click', () => {
        initBoard();
        msgEl.className = 'message hidden';
    });

    // Start
    initBoard();
});
