# Project 1 - Test Case Generator

This project generates test cases from user stories using a local LLM (Ollama).

## Prerequisites

- **Python 3.8+**
- **Node.js & npm**
- **Ollama** running locally with `qwen2.5-coder:1.5b` (or configured model).
  - Install Ollama from [ollama.com](https://ollama.com).
  - Run `ollama pull qwen2.5-coder:1.5b`.
  - Start Ollama: `ollama serve`.

## Quick Start (Windows)

1.  **Clone the repository**:
    ```powershell
    git clone <repository-url>
    cd Project1-TestCaseGenerator
    ```

2.  **Run the startup script**:
    ```powershell
    .\start_project.ps1
    ```
    This script will:
    - Set up the Python virtual environment and install backend dependencies.
    - Install frontend dependencies (npm).
    - Start the Flask backend server.
    - Start the React frontend server.

## Manual Setup

If you prefer to run components manually:

### Backend

1.  Navigate to `backend`:
    ```bash
    cd backend
    ```
2.  Create and activate virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    python app.py
    ```

### Frontend

1.  Navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```

## Usage

1.  Open the web app (usually http://localhost:5173).
2.  Enter a feature description.
3.  Click "Generate Test Cases".
