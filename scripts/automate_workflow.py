import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import generate_text, generate_json
from core.prompt_templates import SUMMARIZE_PROMPT, EXTRACT_JSON_PROMPT, EMAIL_DRAFT_PROMPT, REPORT_PROMPT

def run_full_workflow(raw_text: str):
    print("Starting AI Automation Workflow...\n")

    # Step 1: Summarize the text
    print("--- Step 1: Summarizing Text ---")
    summary_prompt = SUMMARIZE_PROMPT.format(text=raw_text)
    summary = generate_text(summary_prompt)
    print(summary + "\n")

    # Step 2: Extract Key Entities
    print("--- Step 2: Extracting Entities ---")
    schema = '{"topics": ["string"], "key_figures_or_dates": ["string"], "sentiment": "string"}'
    extract_prompt = EXTRACT_JSON_PROMPT.format(schema=schema, text=raw_text)
    extracted_data = generate_json(extract_prompt)
    print(extracted_data + "\n")

    # Step 3: Draft an Email
    print("--- Step 3: Drafting Email ---")
    email_prompt = EMAIL_DRAFT_PROMPT.format(
        topic="Workflow Automation Results",
        tone="professional",
        key_points=f"- Summary: {summary[:100]}...\n- Extracted Data: {extracted_data}"
    )
    email_draft = generate_text(email_prompt)
    print(email_draft + "\n")

    # Step 4: Create a Final Report
    print("--- Step 4: Creating Final Report ---")
    report_data = f"Original Text Length: {len(raw_text)}\nSummary: {summary}\nEntities: {extracted_data}\nAction: Email Drafted."
    report_prompt = REPORT_PROMPT.format(data=report_data)
    report = generate_text(report_prompt)
    print(report + "\n")

    print("Workflow Complete!")

if __name__ == "__main__":
    sample_meeting_transcript = """
    Alice: Welcome everyone to the Q3 planning meeting. Today is September 1st, 2023. Let's start with revenue.
    Bob: Thanks Alice. Q2 revenue was $2.5 million, which is a 20% increase from Q1. We saw strong growth in the enterprise sector.
    Charlie: However, our customer acquisition cost (CAC) increased by 5% to $150 per user. We need to optimize our ad spend.
    Alice: Agreed. Let's aim to reduce CAC back to $140 by the end of Q3. Bob, can you lead the marketing audit?
    Bob: Yes, I'll have a preliminary report by next Wednesday.
    """
    run_full_workflow(sample_meeting_transcript)
