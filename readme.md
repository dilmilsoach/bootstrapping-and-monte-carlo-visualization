# 📊 Statistical Simulation Lab: Bootstrap vs. Monte Carlo

An interactive web application built with **Flask**, **NumPy**, and **Plotly** to visualize the mechanics of bootstrapping and monte carlo.

## 🚀 Live Demo
https://bootstrapping-and-monte-carlo.onrender.com/

---

## 🧐 What This Project Solves
In statistics, we often rely on a single sample to estimate a population mean. But how much can we trust that number? This tool allows users to visualize uncertainty by simulating thousands of "what-if" scenarios.

### The 3-Step Logic
This app breaks the simulation down into three distinct phases:
1. **Step 1: The Population Model** – Defining the "Theoretical World" (Normal, Uniform, Exponential, or Log-Normal) or using the **Empirical Distribution** (Bootstrapping).
2. **Step 2: Virtual Evidence** – Taking a single random sample of size $n$ from that world.
3. **Step 3: The Sampling Distribution** – Repeating the process thousands of times to find the **95% Confidence Interval**.

---

## 💻 Tech Stack
- **Backend:** Python / Flask
- **Computation:** NumPy
- **Visualization:** Plotly
- **Deployment:** Render / Gunicorn

---

## 📈 Learning Outcomes: The Central Limit Theorem
You see how the process works. Another powerful feature of this lab is observing that **no matter what distribution you choose in Step 1** (even a flat Uniform or a skewed Exponential), **Step 3 will always converge into a Gaussian (Normal) distribution.** This is the visual proof of the Central Limit Theorem.

## Built by @dilmilsoach
## ⚙️ Local Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Visit `http://127.0.0.1:5000` in your browser.
