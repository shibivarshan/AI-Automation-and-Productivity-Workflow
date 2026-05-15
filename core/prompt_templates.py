# Prompt templates for different automation tasks

SUMMARIZE_PROMPT = """
You are an expert summarizer. Please summarize the following text.
Make it concise and capture the main points.

Text to summarize:
{text}

Summary:
"""

EMAIL_DRAFT_PROMPT = """
You are a professional assistant. Please draft an email based on the following details.

Topic: {topic}
Tone: {tone}
Key Points:
{key_points}

Email Draft:
"""

EXTRACT_JSON_PROMPT = """
You are a precise data extraction tool. Extract the required entities from the text.
Output MUST be valid JSON based on this schema:
{schema}

Text:
{text}
"""

REPORT_PROMPT = """
You are a professional reporting assistant. Compile the following data into a well-structured report.
Include an executive summary, main body with bullet points, and a conclusion.

Data:
{data}

Report:
"""
