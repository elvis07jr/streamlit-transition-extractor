from docx import Document
import re

def extract_article_data_logic(doc_path):
    document = Document(doc_path)
    paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    articles_found = []
    i = 0
    while i < len(paragraphs):
        current_header = None
        current_narrative = ""
        current_transitions_listed = []
        if re.match(r'^\d+\s+du\s+\d{1,2}/\d{1,2}\s*$', paragraphs[i]):
            current_header = paragraphs[i]
            article_block_start_idx = i
            marker_index = -1
            for j in range(i + 1, len(paragraphs)):
                if "À savoir également dans votre département" in paragraphs[j]:
                    marker_index = j
                    break
            if marker_index != -1:
                narrative_start_idx = -1
                for k in range(marker_index + 1, len(paragraphs)):
                    if len(paragraphs[k]) > 100:
                        current_narrative = paragraphs[k]
                        narrative_start_idx = k
                        break
                if current_narrative:
                    potential_transitions = []
                    next_article_header_idx = len(paragraphs)
                    for l in range(narrative_start_idx + 1, len(paragraphs)):
                        if re.match(r'^\d+\s+du\s+\d{1,2}/\d{1,2}\s*$', paragraphs[l]):
                            next_article_header_idx = l
                            break
                    for m in range(narrative_start_idx + 1, next_article_header_idx):
                        if "Transitions :" in paragraphs[m] and 0 < len(paragraphs[m]) < 50:
                            continue
                        if 0 < len(paragraphs[m]) < 100:
                            potential_transitions.append(paragraphs[m])
                    final_transitions = [t for t in potential_transitions if t.strip()]
                    current_transitions_listed = final_transitions[-3:]
                if current_header and current_narrative and current_transitions_listed:
                    articles_found.append({
                        "header": current_header,
                        "narrative_paragraph": current_narrative,
                        "transitions_listed": current_transitions_listed
                    })
                    i = next_article_header_idx
                    continue
        i += 1
    return articles_found

def extract_triplets_logic(narrative_paragraph, transitions_listed):
    extracted_examples = []
    for transition in transitions_listed:
        transition_escaped = re.escape(transition)
        matches = list(re.finditer(transition_escaped, narrative_paragraph))
        for match in matches:
            start_index = match.start()
            end_index = match.end()
            paragraph_a = narrative_paragraph[:start_index].strip()
            paragraph_b = narrative_paragraph[end_index:].strip()
            if paragraph_a and paragraph_b:
                extracted_examples.append({
                    "paragraph_a": paragraph_a,
                    "transition": transition,
                    "paragraph_b": paragraph_b
                })
    return extracted_examples