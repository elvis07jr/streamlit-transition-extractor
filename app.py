import streamlit as st
import os
import shutil
import uuid
import json
from data_processing import extract_article_data_logic, extract_triplets_logic
from utils import generate_outputs_logic

def file_upload_canvas():
    st.header("1. Upload Your Document")
    uploaded_file = st.file_uploader("Upload your .docx file", type=["docx"], key="docx_uploader")
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    session_temp_dir = os.path.join("temp_uploads", st.session_state['session_id'])
    os.makedirs(session_temp_dir, exist_ok=True)
    if uploaded_file is not None:
        current_uploaded_file_identifier = (uploaded_file.name, uploaded_file.size)
        if 'last_uploaded_file_identifier' in st.session_state and \
           st.session_state['last_uploaded_file_identifier'] != current_uploaded_file_identifier:
            st.session_state['all_extracted_examples'] = []
            st.session_state['all_listed_transitions_raw'] = []
            st.info("New file detected. Clearing previous processing results.")
        temp_file_path = os.path.join(session_temp_dir, uploaded_file.name)
        if not os.path.exists(temp_file_path) or \
           os.path.getsize(temp_file_path) != uploaded_file.size:
            with open(temp_file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.success("File uploaded successfully! Ready for processing.")
            st.session_state['uploaded_file_path'] = temp_file_path
            st.session_state['last_uploaded_file_identifier'] = current_uploaded_file_identifier
        else:
            st.info("File already uploaded and ready for processing.")
            st.session_state['uploaded_file_path'] = temp_file_path
    else:
        st.session_state['uploaded_file_path'] = None

def data_processing_canvas():
    uploaded_file_path = st.session_state.get('uploaded_file_path', None)
    st.header("2. Process Document")
    if uploaded_file_path:
        if st.button("Start Extraction", key="start_extraction_button"):
            st.info("Extracting article data and transitions...")
            try:
                articles_data = extract_article_data_logic(uploaded_file_path)
                all_extracted_examples = []
                all_listed_transitions_raw = []
                for article in articles_data:
                    all_listed_transitions_raw.extend(article["transitions_listed"])
                    if article["narrative_paragraph"] and article["transitions_listed"]:
                        examples = extract_triplets_logic(article["narrative_paragraph"], article["transitions_listed"])
                        all_extracted_examples.extend(examples)
                st.success("Extraction complete!")
                st.session_state['all_extracted_examples'] = all_extracted_examples
                st.session_state['all_listed_transitions_raw'] = all_listed_transitions_raw
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
                st.error("Please ensure your document structure matches the expected format (Header, Title/Blurb, Marker, Narrative, 2-3 Transitions).")
                st.session_state['all_extracted_examples'] = []
                st.session_state['all_listed_transitions_raw'] = []
    else:
        st.info("Please upload a .docx file in the 'Upload Your Document' section first.")

def display_results_canvas():
    num_examples = len(st.session_state.get('all_extracted_examples', []))
    st.header("3. Extraction Summary")
    if num_examples > 0:
        st.write(f"Total valid few-shot examples extracted: **{num_examples}**")
    else:
        st.info("No examples extracted yet. Upload a document and start extraction.")

def output_generation_canvas():
    all_extracted_examples = st.session_state.get('all_extracted_examples', [])
    all_listed_transitions_raw = st.session_state.get('all_listed_transitions_raw', [])
    if all_extracted_examples or all_listed_transitions_raw:
        st.header("4. Generate and Save Outputs")
        st.subheader("Select Output Files to Generate")
        col1, col2, col3 = st.columns(3)
        generate_fewshot_json = col1.checkbox("fewshot_examples.json")
        generate_fewshots_rejected_txt = col1.checkbox("fewshots_rejected.txt")
        generate_transitions_txt = col2.checkbox("transitions_only.txt")
        generate_transitions_rejected_txt = col2.checkbox("transitions_only_rejected.txt")
        generate_fewshot_jsonl = col3.checkbox("fewshot_examples.jsonl")
        generate_finetuning_rejected_txt = col3.checkbox("fewshots-fineTuning_rejected.txt")
        if st.button("Generate and Save Selected Outputs", key="generate_outputs_button"):
            st.info("Generating output files...")
            outputs = generate_outputs_logic(all_extracted_examples, all_listed_transitions_raw)
            output_dir = "extracted_data"
            os.makedirs(output_dir, exist_ok=True)
            if generate_fewshot_json:
                output_path = os.path.join(output_dir, "fewshot_examples.json")
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(outputs["fewshot_examples.json"], f, indent=4, ensure_ascii=False)
                st.success(f"Saved `fewshot_examples.json` to `{output_path}`")
                st.download_button(
                    label="Download fewshot_examples.json",
                    data=json.dumps(outputs["fewshot_examples.json"], indent=4, ensure_ascii=False).encode('utf-8'),
                    file_name="fewshot_examples.json",
                    mime="application/json",
                    key="dl_fewshot_json"
                )
            if generate_fewshots_rejected_txt:
                output_path = os.path.join(output_dir, "fewshots_rejected.txt")
                content = "\n".join(outputs["fewshots_rejected.txt"])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success(f"Saved `fewshots_rejected.txt` to `{output_path}`")
                st.download_button(
                    label="Download fewshots_rejected.txt",
                    data=content.encode('utf-8'),
                    file_name="fewshots_rejected.txt",
                    mime="text/plain",
                    key="dl_fewshots_rejected_txt"
                )
            if generate_transitions_txt:
                output_path = os.path.join(output_dir, "transitions_only.txt")
                content = "\n".join(outputs["transitions_only.txt"])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success(f"Saved `transitions_only.txt` to `{output_path}`")
                st.download_button(
                    label="Download transitions_only.txt",
                    data=content.encode('utf-8'),
                    file_name="transitions_only.txt",
                    mime="text/plain",
                    key="dl_transitions_txt"
                )
            if generate_transitions_rejected_txt:
                output_path = os.path.join(output_dir, "transitions_only_rejected.txt")
                content_lines = [f"{t}: {count}" for t, count in outputs["transitions_only_rejected.txt"].items()]
                content = "\n".join(content_lines)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success(f"Saved `transitions_only_rejected.txt` to `{output_path}`")
                st.download_button(
                    label="Download transitions_only_rejected.txt",
                    data=content.encode('utf-8'),
                    file_name="transitions_only_rejected.txt",
                    mime="text/plain",
                    key="dl_transitions_rejected_txt"
                )
            if generate_fewshot_jsonl:
                output_path = os.path.join(output_dir, "fewshot_examples.jsonl")
                content = "\n".join(outputs["fewshot_examples.jsonl"])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success(f"Saved `fewshot_examples.jsonl` to `{output_path}`")
                st.download_button(
                    label="Download fewshot_examples.jsonl",
                    data=content.encode('utf-8'),
                    file_name="fewshot_examples.jsonl",
                    mime="application/jsonlines",
                    key="dl_fewshot_jsonl"
                )
            if generate_finetuning_rejected_txt:
                output_path = os.path.join(output_dir, "fewshots-fineTuning_rejected.txt")
                content = "\n".join(outputs["fewshots-fineTuning_rejected.txt"])
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success(f"Saved `fewshots-fineTuning_rejected.txt` to `{output_path}`")
                st.download_button(
                    label="Download fewshots-fineTuning_rejected.txt",
                    data=content.encode('utf-8'),
                    file_name="fewshots-fineTuning_rejected.txt",
                    mime="text/plain",
                    key="dl_finetuning_rejected_txt"
                )
    else:
        st.info("Upload a document and click 'Start Extraction' to enable output generation.")

def main():
    st.set_page_config(layout="wide", page_title="Transition Phrase Extractor")
    st.title("🇫🇷 Transition Phrase Extractor for French News Articles")
    st.markdown("""
    Upload a `.docx` file containing regional French news articles to extract structured examples of transition phrases.
    The app will generate datasets for downstream analysis and AI fine-tuning.
    """)
    if 'all_extracted_examples' not in st.session_state:
        st.session_state['all_extracted_examples'] = []
    if 'all_listed_transitions_raw' not in st.session_state:
        st.session_state['all_listed_transitions_raw'] = []
    if 'uploaded_file_path' not in st.session_state:
        st.session_state['uploaded_file_path'] = None
    if 'last_uploaded_file_identifier' not in st.session_state:
        st.session_state['last_uploaded_file_identifier'] = None
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    file_upload_canvas()
    data_processing_canvas()
    display_results_canvas()
    output_generation_canvas()
    st.markdown("""
    ---
    **How to use:**
    1.  **Upload** your `.docx` file using the file uploader.
    2.  Click **"Start Extraction"** to process the document.
    3.  View the **Extraction Summary** (number of few-shot examples).
    4.  **Select** which output files you wish to generate and click **"Generate and Save Selected Outputs"**.
    """)
    @st.cache_data(show_spinner=False, ttl=3600)
    def cleanup_old_temp_dirs(current_session_id):
        base_temp_dir = "temp_uploads"
        if os.path.exists(base_temp_dir):
            for item in os.listdir(base_temp_dir):
                item_path = os.path.join(base_temp_dir, item)
                if os.path.isdir(item_path) and item != current_session_id:
                    try:
                        shutil.rmtree(item_path)
                    except OSError as e:
                        pass
    cleanup_old_temp_dirs(st.session_state['session_id'])

if __name__ == "__main__":
    main()