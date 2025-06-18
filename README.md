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
