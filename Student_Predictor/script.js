document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const output = document.getElementById('prediction-output');

    // --- Machine Learning Implementation (Multiple Linear Regression) ---
    
    // We will generate synthetic data and train the model using Gradient Descent right in the browser!
    let weights = [0, 0, 0, 0];
    let bias = 0;

    function generateDataAndTrain() {
        const n_samples = 200;
        const X = [];
        const y = [];

        // Generate synthetic data
        for (let i = 0; i < n_samples; i++) {
            const hours = Math.random() * 9 + 1; // 1 to 10
            const attendance = Math.random() * 50 + 50; // 50 to 100
            const prev = Math.random() * 60 + 40; // 40 to 100
            const assigns = Math.floor(Math.random() * 11); // 0 to 10
            
            // The underlying true function (with some noise)
            let score = (hours * 3.5) + (attendance * 0.3) + (prev * 0.4) + (assigns * 1.5);
            score += (Math.random() - 0.5) * 10; // Noise
            score = Math.min(Math.max(score, 0), 100);

            X.push([hours, attendance, prev, assigns]);
            y.push(score);
        }

        // Normalize features for stable Gradient Descent
        const means = [0, 0, 0, 0];
        const stds = [0, 0, 0, 0];
        
        for (let j = 0; j < 4; j++) {
            let sum = 0;
            for (let i = 0; i < n_samples; i++) sum += X[i][j];
            means[j] = sum / n_samples;
            
            let varSum = 0;
            for (let i = 0; i < n_samples; i++) varSum += Math.pow(X[i][j] - means[j], 2);
            stds[j] = Math.sqrt(varSum / n_samples);
        }

        const X_norm = X.map(row => row.map((val, j) => (val - means[j]) / stds[j]));

        // Gradient Descent Training
        const learning_rate = 0.1;
        const epochs = 500;
        
        let w = [0, 0, 0, 0];
        let b = 0;

        for (let epoch = 0; epoch < epochs; epoch++) {
            let dw = [0, 0, 0, 0];
            let db = 0;

            for (let i = 0; i < n_samples; i++) {
                let y_pred = b;
                for (let j = 0; j < 4; j++) y_pred += w[j] * X_norm[i][j];
                
                const error = y_pred - y[i];
                db += error;
                for (let j = 0; j < 4; j++) dw[j] += error * X_norm[i][j];
            }

            b -= learning_rate * (db / n_samples);
            for (let j = 0; j < 4; j++) {
                w[j] -= learning_rate * (dw[j] / n_samples);
            }
        }

        return { w, b, means, stds };
    }

    // Train the model on load
    const model = generateDataAndTrain();
    console.log("Model trained successfully in browser:", model);

    function predict(hours, attendance, prev, assigns) {
        const input = [hours, attendance, prev, assigns];
        const { w, b, means, stds } = model;
        
        let prediction = b;
        for (let j = 0; j < 4; j++) {
            const normalized_val = (input[j] - means[j]) / stds[j];
            prediction += w[j] * normalized_val;
        }
        
        return Math.min(Math.max(prediction, 0), 100);
    }

    // Handle form submission
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const hours = parseFloat(document.getElementById('hours').value);
        const attendance = parseFloat(document.getElementById('attendance').value);
        const prev = parseFloat(document.getElementById('prev-score').value);
        const assigns = parseFloat(document.getElementById('assignments').value);

        const score = predict(hours, attendance, prev, assigns);
        
        // Animate counter
        let current = 0;
        const target = score;
        const interval = setInterval(() => {
            current += target / 20;
            if (current >= target) {
                current = target;
                clearInterval(interval);
            }
            output.textContent = `${current.toFixed(2)} / 100`;
        }, 20);
    });
});
