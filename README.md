# Draconic Case Study: Customer Support Ticket Analyzer

This project implements a multi-agent AI system to analyze and route customer support tickets, built using Pydantic and Google Gemini Flash 2.0.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Setup and Installation](#3-setup-and-installation)
4. [Usage](#4-usage)
5. [Evaluation](#5-evaluation)
6. [Deliverables](#6-deliverables)
7. [Design Decisions & Rationale](#7-design-decisions--rationale)
8. [What Didn't Work and Why](#8-what-didnt-work-and-why)
9. [Interesting Test Case Behaviors](#9-interesting-test-case-behaviors)

## 1. Project Overview

The goal of this project is to build a robust multi-agent system that can:

* Analyze the sentiment of incoming customer support tickets.
* Assign an appropriate priority level based on various factors.
* Route the ticket to the correct department for efficient resolution.

This system leverages Google Gemini Flash 2.0 for its AI capabilities, structured with Pydantic for clear data models and inter-agent communication. The system also includes an automated evaluation suite to verify accuracy across multiple metrics.

## 2. System Architecture

Detailed architecture and rationale can be found in [`docs/architecture.md`](docs/architecture.md).

In brief, the system consists of three sequential specialized agents:

1. **Sentiment Agent:** Determines the emotional tone and urgency.
2. **Priority Agent:** Assigns a priority based on sentiment and customer data.
3. **Router Agent:** Routes the ticket to the appropriate department.

Each agent is powered by Google's Gemini model and communicates via structured Pydantic models, making the system modular and easily extendable.

## 3. Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jbittu/bittu_jaiswal_case_study.git
   cd bittu_jaiswal_case_study
   ```
2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**

   * **On macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```
   * **On Windows:**

     ```bash
     venv\Scripts\activate
     ```
4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
5. **Set up your Google API Key:**
   Create a `.env` file in the root directory of the project and add your Google Gemini API key:

   ```env
   GOOGLE_API_KEY="YOUR_GOOGLE_FLASH_API_KEY_HERE"
   ```

   **Note:** Replace the placeholder with your actual API key.

## 4. Usage

To process a support ticket via CLI using the `main.py` script:

```bash
python main.py
```

To run the complete evaluation test suite:

```bash
pytest tests/test_end_to_end.py -s
```

## 5. Evaluation

An `Evaluator` class tracks the accuracy of sentiment classification, priority assignment, and department routing. Results are printed to console and saved to `evaluation_report.json`.

Each ticket is compared against ground truth annotations and logged with detailed feedback.

## 6. Deliverables

* 🧠 AI Agent Implementations (`agents/`)
* 📦 Data Models (`shared_models.py`)
* 🧪 Test Suite & Ground Truth (`tests/`)
* 🛠 Orchestration Logic (`main.py`)
* 📊 Evaluation Report (`evaluation_report.json`)
* 📄 Architecture Document (`docs/architecture.md`)

## 7. Design Decisions & Rationale

* Modular agents improve maintainability and interpretability.
* Prompt engineering ensures accurate and deterministic JSON outputs.
* Gemini Flash 2.0 was chosen for its speed and sufficient accuracy.
* Enum-based data models prevent schema drift between agents.
* Clear reasoning fields help trace and debug decision-making.

## 8. What Didn't Work and Why

* Initial prompt templates allowed ambiguity in routing labels (e.g., "tech support" vs. "technical\_support") — resolved via strict enum matching.
* Model responses with extraneous text (e.g., "Sure, here's your JSON") caused parsing errors — solved using `response_mime_type="application/json"`.

## 9. Interesting Test Case Behaviors

* Feature requests written calmly are correctly classified as **positive**.
* Outages with harsh language trigger both **urgent** sentiment and **critical** priority.
* Enterprise users reporting minor bugs often still receive **medium** priority due to high revenue and age.
