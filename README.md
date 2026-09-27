# 🤖 AI Code Tutor & Bug Explainer

An AI-powered web application that helps users write, analyze, execute, debug, and understand code with the help of Artificial Intelligence.

The application provides code analysis, error explanation, line-by-line code explanation, code execution, automatic fix suggestions, code history, and an interactive AI Tutor.

---

## 📌 Project Overview

**AI Code Tutor & Bug Explainer** is a web-based learning and debugging platform designed to help students and beginner programmers understand programming concepts and identify errors in their code.

Instead of only displaying an error message, the application uses AI to explain:

- What went wrong
- Why the error occurred
- Which line caused the problem
- How the code can be corrected
- How the corrected code works

The application also allows users to execute code directly from the browser and interact with an AI Tutor for programming-related questions.

---

## ✨ Features

### 🔍 1. Code Analysis

Analyze the submitted code using AI and receive an explanation of the code, potential issues, and suggestions for improvement.

### 🐛 2. Bug & Error Explanation

The application identifies runtime errors and provides an AI-generated explanation of the problem.

It can provide information such as:

- Error type
- Error line
- Cause of the error
- Suggested solution
- Corrected code

### ▶️ 3. Code Execution

Users can execute code directly from the web application.

Supported programming languages:

- Python
- C
- C++
- Java
- JavaScript

### 💡 4. AI Suggested Fix

When an error occurs, the AI can generate corrected code.

The user can review the suggested solution and apply the corrected code to the editor.

### 📖 5. Line-by-Line Explanation

The application can explain code line by line in a beginner-friendly manner.

This helps students understand what each part of their program does.

### 🤖 6. AI Tutor

Users can ask programming questions through the integrated AI Tutor.

The tutor supports different learning levels:

- Beginner
- Intermediate
- Advanced

### 📚 7. Code History

Analyzed code can be stored in the application history.

Users can:

- View previous code
- Load previous code
- Delete history records

### 🧹 8. Clear & Sample Code

The editor provides options to:

- Clear the current code
- Load sample programs
- Select different programming languages

### 💻 9. Developer-Friendly Interface

The application provides a modern dark-themed interface with:

- Code editor
- Analysis section
- Terminal output
- AI Tutor
- Code history
- Language selection

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask

### Artificial Intelligence

- Google Gemini API

### Database

- SQLite

### Programming Languages Supported

- Python
- C
- C++
- Java
- JavaScript

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 🏗️ Project Architecture

```text
                     ┌───────────────────────┐
                     │       User            │
                     │   Web Browser         │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │      Frontend         │
                     │   HTML / CSS / JS     │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │    Flask Backend      │
                     │       app.py          │
                     └───────────┬───────────┘
                           ┌─────┴─────┐
                           │           │
                           ▼           ▼
                 ┌──────────────┐  ┌───────────────┐
                 │ Gemini AI    │  │ Code Executor │
                 │ API          │  │               │
                 └──────────────┘  └───────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ SQLite Database  │
                  │ Code History     │
                  └──────────────────┘
