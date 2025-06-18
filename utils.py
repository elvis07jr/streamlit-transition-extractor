import json
from collections import Counter

def generate_outputs_logic(extracted_examples, listed_transitions_raw):
    outputs = {
        "fewshot_examples.json": [],
        "fewshots_rejected.txt": [],
        "transitions_only.txt": [],
        "transitions_only_rejected.txt": {},
        "fewshot_examples.jsonl": [],
        "fewshots-fineTuning_rejected.txt": []
    }

    for example in extracted_examples:
        try:
            if not all(k in example for k in ["paragraph_a", "transition", "paragraph_b"]):
                raise ValueError("Missing required keys in example.")
            if not (isinstance(example["paragraph_a"], str) and 
                    isinstance(example["transition"], str) and 
                    isinstance(example["paragraph_b"], str)):
                raise ValueError("Example values must be strings.")
            if not (example["paragraph_a"].strip() and 
                    example["transition"].strip() and 
                    example["paragraph_b"].strip()):
                raise ValueError("Example values cannot be empty strings.")

            outputs["fewshot_examples.json"].append(example)
            prompt = example["paragraph_a"] + " " + example["transition"]
            completion = example["paragraph_b"]
            outputs["fewshot_examples.jsonl"].append(json.dumps({"prompt": prompt, "completion": completion}, ensure_ascii=False))

        except ValueError as e:
            outputs["fewshots_rejected.txt"].append(
                f"Rejected Few-shot Example: {json.dumps(example, ensure_ascii=False)}. Reason: {e}"
            )
        except Exception as e:
            outputs["fewshots_rejected.txt"].append(
                f"Rejected Few-shot Example (Unexpected Error): {json.dumps(example, ensure_ascii=False)}. Error: {e}"
            )

    all_unique_transitions = []
    rejected_transitions_counter = Counter()

    for transition_group in listed_transitions_raw:
        for transition in transition_group:
            cleaned_transition = transition.strip()
            if cleaned_transition and 0 < len(cleaned_transition) < 100:
                if cleaned_transition not in all_unique_transitions:
                    all_unique_transitions.append(cleaned_transition)
            else:
                rejected_transitions_counter[cleaned_transition if cleaned_transition else "[EMPTY/TOO LONG]"] += 1

    outputs["transitions_only.txt"] = sorted(all_unique_transitions)
    outputs["transitions_only_rejected.txt"] = dict(rejected_transitions_counter)

    if outputs["fewshots_rejected.txt"]:
        outputs["fewshots-fineTuning_rejected.txt"].extend(outputs["fewshots_rejected.txt"])
        outputs["fewshots-fineTuning_rejected.txt"].append("\n--- Summary of Rejected Fine-tuning Examples ---")
        outputs["fewshots-fineTuning_rejected.txt"].append(f"Total rejected: {len(outputs['fewshots_rejected.txt'])}")
    else:
        outputs["fewshots-fineTuning_rejected.txt"].append("No few-shot examples were rejected for fine-tuning.")

    return outputs