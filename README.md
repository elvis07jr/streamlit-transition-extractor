# French Transitions Extractor

## Project Description

The French Transitions Extractor is a Streamlit-based Python application designed to streamline the process of extracting structured linguistic data from `.docx` documents. Specifically, it focuses on identifying "triplets" composed of a preceding paragraph (`paragraph_a`), a transitional phrase (`transition`), and a succeeding paragraph (`paragraph_b`). Additionally, it compiles a comprehensive list of all unique transitional phrases encountered across the processed documents.

This tool is particularly useful for Natural Language Processing (NLP) tasks, linguistic analysis, or dataset generation where specific contextual examples of transitions are required.

## Features

* **`.docx` Document Processing:** Upload and parse Word documents.
* **Article Structure Recognition:** Identifies distinct articles based on a predefined header and marker-based structure.
* **Triplet Extraction:** Extracts `(paragraph_a, transition, paragraph_b)` triplets suitable for few-shot learning or fine-tuning language models.
* **Unique Transition Listing:** Compiles a sorted list of all unique transitional phrases found.
* **Multiple Output Formats:** Generates data in `.json`, `.jsonl`, and `.txt` formats for various use cases.
* **Rejection Logging:** Provides logs for examples or transitions that fail validation criteria during extraction.
* **User-Friendly Interface:** Intuitive web interface built with Streamlit for ease of use.

## Getting Started

Follow these instructions to set up and run the application on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+**
* **Git**

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/elvis07jr/streamlit-transition-extractor.git](https://github.com/elvis07jr/streamlit-transition-extractor.git)
    cd streamlit-transitions-extractor
    ```
  
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Project Structure

The project is organized as follows:
French-Transitions-Extractor/
├── app.py                     # Main Streamlit application
├── data_processing.py         # Contains logic for parsing DOCX and extracting articles/triplets
├── utils.py                   # Helper functions for generating various output file formats
├── requirements.txt           # List of Python dependencies
└── README.md                  # This README file

## Usage

1.  **Place your `.docx` files:** Ensure the Word documents you wish to process (e.g., `word10.docx`, `word374.docx`) are accessible on your computer. You can place them directly in the project directory for convenience, or browse to their location during upload.

2.  **Run the Streamlit application:**
    With your virtual environment activated, navigate to the project's root directory in your terminal and run:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser.

3.  **Process Documents:**
    * In the web interface, use the "1. Upload Your Document" section to upload a `.docx` file.
    * Click "2. Start Extraction" to initiate the data processing.
    * Review the "3. Extraction Summary" for a high-level overview of the extracted examples.
    * In "4. Generate and Save Outputs," select the desired output file formats (e.g., `fewshot_examples.json`, `transitions_only.txt`).
    * Click "Generate and Save Selected Outputs" to download the files to your local machine.
---
Compiled by: https://github.com/elvis07jr
Email: tile.pc@hotmail.com
---
## License

This project is licensed under the MIT License - see the `LICENSE` file (if you create one) for details.
