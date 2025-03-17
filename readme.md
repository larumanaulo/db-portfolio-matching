## Property Portfolio Reconciliation Tool
 This tool reconciles two lists of properties by finding matching elements and identifying discrepancies in descriptions, limits, and mortgage amounts.

## Solution

The solution revolves around splitting the second portfolio property list properties in batches and for each batch we analise chunks from the first portfolio. It basically compares each property from portfolio2 to all the properties in portfolio 1 but in batches and chunks of properties at the time. 
The main reason why I have went with splitting it in multiple paralell execution blocks is for it to be able to support long property lists without the risk of reaching API request limits and LLM Input token limitations.

The program could benefit from refactoring and some things arte overcomplicated, but that's mainly because I have user code generating LLM to create some tools fast. Tools like in data_utils.py.



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
