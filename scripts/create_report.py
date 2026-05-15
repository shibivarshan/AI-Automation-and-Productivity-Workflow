import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import generate_text
from core.prompt_templates import REPORT_PROMPT
from core.validators import ReportInput
from pydantic import ValidationError

def create_report(data: str):
    try:
        validated_input = ReportInput(data=data)
    except ValidationError as e:
        print(f"Input Validation Error:\n{e}")
        return

    prompt = REPORT_PROMPT.format(data=validated_input.data)
    
    print("Generating report...")
    report = generate_text(prompt)
    print("\n--- Final Report ---\n")
    print(report)
    print("\n--------------------")

if __name__ == "__main__":
    raw_data = """
    - Q1 Revenue: $1.2M (up 15% YoY)
    - New User Signups: 15,000
    - Server uptime: 99.99%
    - Marketing spend: $50,000
    - Customer churn rate increased by 2%
    """
    create_report(raw_data)
