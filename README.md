# 🏦 Financial Tracking & Banking Engine

A robust, object-oriented financial management system built with Python. Developed as a Semester 1 Milestone Project, this application focuses on core software engineering principles: encapsulation, defensive runtime validation, persistent CSV ledger tracking, and an interactive prototype interface built with Streamlit.

---

## 🌐 Live Prototype Demo

Experience the live interactive application in your browser:  
🔗 **[Live Streamlit App](https://expensetracker-24lcwpqyqcxzm3ayxqokkq.streamlit.app/)**

---

## 📌 Architecture & Design

The project separates core business logic from user interaction:
- **Backend Core Engine (`main.py`)**: Built from the ground up using pure Python OOP concepts, handling data persistence and defensive logic.
- **Interactive UI (`app.py`)**: A Streamlit frontend providing real-time metric tracking, form validation, and balance visualization based on the core engine.

---

## 🚀 Key Features

* **Object-Oriented Encapsulation**: Enforces private state protection (`__balance`) with controlled getter methods to prevent unauthorized balance mutation.
* **Defensive Error Boundaries**: Wraps input pipelines in `try...except ValueError` blocks, ensuring bad or malformed inputs never crash the session.
* **Domain Logic Protection**: Rejects negative deposit/debit requests and provides overdraft protection when withdrawals exceed available funds.
* **Persistent CSV Logging**: Appends transaction histories (`credit`, `debit`, running balance) into `save_to_file.csv` to maintain audit trails across sessions.

---

## 🛠️ Tech Stack

* **Language**: Python 3
* **Frontend / Dashboard**: Streamlit
* **Storage**: CSV (Flat-file data persistence)
* **Design Pattern**: Object-Oriented Programming (OOP)
* **Version Control**: Git & GitHub

---
