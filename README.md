# Draconic Case Study: Customer Support Ticket Analyzer

This project implements a multi-agent AI system to analyze and route customer support tickets, built using Pydantic AI and Google Gemini Flash 2.0.

## Table of Contents

1.  [Project Overview](#1-project-overview)
2.  [System Architecture](#2-system-architecture)
3.  [Setup and Installation](#3-setup-and-installation)
4.  [Usage](#4-usage)
5.  [Evaluation](#5-evaluation)
6.  [Deliverables](#6-deliverables)
7.  [Design Decisions & Rationale](#7-design-decisions--rationale)
8.  [What Didn't Work and Why](#8-what-didnt-work-and-why)
9.  [Interesting Test Case Behaviors](#9-interesting-test-case-behaviors)

## 1. Project Overview

The goal of this project is to build a robust multi-agent system that can:
* Analyze the sentiment of incoming customer support tickets.
* Assign an appropriate priority level based on various factors.
* Route the ticket to the correct department for efficient resolution.

This system leverages Google Gemini Flash 2.0 for its AI capabilities, structured with Pydantic for clear data models and inter-agent communication.

## 2. System Architecture

Detailed architecture and rationale can be found in `docs/architecture.md`.

In brief, the system consists of three sequential specialized agents:
1.  **Sentiment Agent:** Determines the emotional tone and urgency.
2.  **Priority Agent:** Assigns a priority based on sentiment and customer data.
3.  **Router Agent:** Routes the ticket to the appropriate department.

## 3. Setup and Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone [https://github.com/your-username/your-name-case-study.git](https://github.com/your-username/your-name-case-study.git)
    cd your-name-case-study
    ```
    (Or create the project structure manually as outlined above).
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    * **On Windows:**
        ```bash
        venv\Scripts\activate
        ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Set up your Google API Key:**
    Create a `.env` file in the root directory of the project and add your Google Gemini Flash 2.0 API key:
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_FLASH_API_KEY_HERE"
    ```
    **Remember to replace `"YOUR_GOOGLE_FLASH_API_KEY_HERE"` with your actual key.**

## 4. Usage

To process an example ticket using the `main.py` script:

```bash
python main.py