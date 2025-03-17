## Property Portfolio Reconciliation Tool
 This tool reconciles two lists of properties by finding matching elements and identifying discrepancies in descriptions, limits, and mortgage amounts.

## Prerequisites

 - Python 3.7 or higher
 - pip (Python package installer)

## Installation

 - Clone or download the repository
 - Download the code to your local machine and navigate to the project directory.
 - Create a virtual environment
 ```bash
 python -m venv env
 ```
 - Activate Virtual Environemnt
 ```bash
 source env/bin/activate
 ```
  - Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
 - Create an `.env` file which holds the OpenAi API Key

 ```bash
 OPENAI_API_KEY=your_api_key_here
 ```

 - Run the program
 ```bash
 python main.py
```

There will be terminal notifications for when the process has finished and the results should be available in `/output/reconciled_requirements.json`