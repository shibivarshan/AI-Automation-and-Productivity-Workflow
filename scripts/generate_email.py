import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import generate_text
from core.prompt_templates import EMAIL_DRAFT_PROMPT
from core.validators import EmailDraftInput
from pydantic import ValidationError

def draft_email(topic: str, tone: str, key_points: list):
    try:
        validated_input = EmailDraftInput(
            topic=topic,
            tone=tone,
            key_points=key_points
        )
    except ValidationError as e:
        print(f"Input Validation Error:\n{e}")
        return

    points_str = "\n".join([f"- {kp}" for kp in validated_input.key_points])
    prompt = EMAIL_DRAFT_PROMPT.format(
        topic=validated_input.topic,
        tone=validated_input.tone,
        key_points=points_str
    )
    
    print("Generating email draft...")
    draft = generate_text(prompt)
    print("\n--- Email Draft ---\n")
    print(draft)
    print("\n-------------------")

if __name__ == "__main__":
    draft_email(
        topic="Project Update Meeting",
        tone="professional but friendly",
        key_points=[
            "Completed the backend integration",
            "Frontend needs some UI tweaks",
            "Let's schedule a 15-minute call tomorrow to discuss next steps"
        ]
    )
