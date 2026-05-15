import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.llm_client import generate_text, generate_json
from core.prompt_templates import SUMMARIZE_PROMPT, EXTRACT_JSON_PROMPT, EMAIL_DRAFT_PROMPT, REPORT_PROMPT
from core.history import log_task, get_history, clear_history
from core.utils import read_file_content

st.set_page_config(page_title="AI Automation Workflow", page_icon="🤖", layout="wide")

# Inject Custom CSS for Premium Aesthetics
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .css-1d391kg {
        background-color: #1E2127;
    }
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        transition: all 0.3s ease;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }
    .stDownloadButton>button {
        background-color: #10B981;
    }
    .stDownloadButton>button:hover {
        background-color: #059669;
    }
    .history-card {
        background: #1E2127;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 12px;
        border-left: 4px solid #4F46E5;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ AI Productivity Hub")
st.markdown("Automate your daily workflows: Summarize, Extract, Draft, and Report. Now with File Uploads and History Tracking!")

if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY is not set. Please add it to your .env file or environment variables.")

# Sidebar Navigation
task = st.sidebar.radio(
    "Select Workflow",
    ["Summarize Text", "Draft Email", "Extract JSON", "Generate Report", "Full Orchestrated Workflow", "Activity History"]
)

# Helper for file upload
def handle_file_upload(label="Upload a document (.txt, .pdf)"):
    uploaded_file = st.file_uploader(label, type=["txt", "pdf"])
    if uploaded_file:
        return read_file_content(uploaded_file)
    return None

if task == "Summarize Text":
    st.header("📝 Summarize Document")
    text_input = handle_file_upload() or st.text_area("Or paste text here:", height=200)
    
    if st.button("Summarize"):
        if text_input:
            with st.spinner("Analyzing and summarizing..."):
                prompt = SUMMARIZE_PROMPT.format(text=text_input)
                result = generate_text(prompt)
                log_task("Summarize", text_input, result)
                st.success("Summary Generated!")
                st.write(result)
                st.download_button("Download Summary", data=result, file_name="summary.txt", mime="text/plain")
        else:
            st.warning("Please provide some text or a file.")

elif task == "Draft Email":
    st.header("✉️ Draft Email")
    topic = st.text_input("Email Topic:")
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent", "Persuasive"])
    key_points = handle_file_upload("Upload notes (.txt, .pdf)") or st.text_area("Or type Key Points (one per line):", height=150)
    
    if st.button("Draft Email"):
        if topic and key_points:
            with st.spinner("Drafting your email..."):
                points_formatted = "\n".join([f"- {p}" for p in key_points.split("\n") if p.strip()])
                prompt = EMAIL_DRAFT_PROMPT.format(topic=topic, tone=tone, key_points=points_formatted)
                result = generate_text(prompt)
                log_task("Email Draft", f"Topic: {topic}\nPoints: {key_points}", result)
                st.success("Email Ready!")
                st.write(result)
                st.download_button("Download Email", data=result, file_name="email_draft.txt", mime="text/plain")
        else:
            st.warning("Please provide a topic and key points.")

elif task == "Extract JSON":
    st.header("🔍 Extract Structured Data")
    text_input = handle_file_upload() or st.text_area("Or paste unstructured text:", height=150)
    schema = st.text_input("JSON Schema / Target Fields", value='{"name": "string", "date": "string"}')
    
    if st.button("Extract"):
        if text_input and schema:
            with st.spinner("Extracting entities..."):
                prompt = EXTRACT_JSON_PROMPT.format(schema=schema, text=text_input)
                result = generate_json(prompt)
                log_task("Extract JSON", text_input, result)
                st.success("Extraction Complete!")
                st.code(result, language="json")
                st.download_button("Download JSON", data=result, file_name="extracted_data.json", mime="application/json")
        else:
            st.warning("Please provide text and a schema.")

elif task == "Generate Report":
    st.header("📊 Compile Report")
    data_input = handle_file_upload("Upload raw data (.txt, .pdf)") or st.text_area("Or paste raw data/notes:", height=200)
    
    if st.button("Create Report"):
        if data_input:
            with st.spinner("Compiling professional report..."):
                prompt = REPORT_PROMPT.format(data=data_input)
                result = generate_text(prompt)
                log_task("Generate Report", data_input, result)
                st.success("Report Generated!")
                st.markdown(result)
                st.download_button("Download Report", data=result, file_name="report.md", mime="text/markdown")
        else:
            st.warning("Please provide data for the report.")

elif task == "Full Orchestrated Workflow":
    st.header("🔄 Full Workflow")
    text_input = handle_file_upload("Upload transcript or long document (.txt, .pdf)") or st.text_area("Or paste text:", height=200)
    
    if st.button("Run Pipeline"):
        if text_input:
            st.info("Running pipeline... this may take a moment.")
            
            # 1. Summarize
            summary = generate_text(SUMMARIZE_PROMPT.format(text=text_input))
            st.subheader("1. Executive Summary")
            st.write(summary)
            
            # 2. Extract
            schema = '{"topics": ["string"], "action_items": ["string"], "key_dates": ["string"]}'
            extracted = generate_json(EXTRACT_JSON_PROMPT.format(schema=schema, text=text_input))
            st.subheader("2. Extracted Entities")
            st.code(extracted, language="json")
            
            # 3. Email
            email_prompt = EMAIL_DRAFT_PROMPT.format(
                topic="Meeting Notes & Next Steps",
                tone="professional",
                key_points=f"- Summary: {summary[:200]}...\n- Action Items: {extracted}"
            )
            email = generate_text(email_prompt)
            st.subheader("3. Follow-up Email Draft")
            st.write(email)
            
            log_task("Full Workflow", text_input, f"Summary:\n{summary}\n\nEmail:\n{email}")
            st.success("Pipeline Complete!")
        else:
            st.warning("Please provide input text.")

elif task == "Activity History":
    st.header("🕰️ Activity History")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("Your recent automation tasks.")
    with col2:
        if st.button("Clear History"):
            clear_history()
            st.rerun()

    history = get_history()
    if not history:
        st.info("No history found. Run some tasks!")
    else:
        for idx, item in enumerate(history):
            st.markdown(f"""
            <div class="history-card">
                <small style="color: #A0AEC0;">{item['timestamp']} • {item['task_type']}</small>
                <div style="margin-top: 8px; font-weight: bold;">Input Preview:</div>
                <div style="font-size: 0.9em; margin-bottom: 8px;">{item['input_preview']}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("View Full Output"):
                st.write(item['output'])
