import sys
import os

# Add parent directory to path to import core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import generate_text
from core.prompt_templates import SUMMARIZE_PROMPT
from core.validators import SummarizeInput
from pydantic import ValidationError

def summarize(text: str):
    try:
        # Validate input
        validated_input = SummarizeInput(text=text)
    except ValidationError as e:
        print(f"Input Validation Error:\n{e}")
        return

    # Format prompt
    prompt = SUMMARIZE_PROMPT.format(text=validated_input.text)
    
    print("Generating summary...")
    summary = generate_text(prompt)
    print("\n--- Summary ---\n")
    print(summary)
    print("\n---------------")

if __name__ == "__main__":
    sample_text = """
    Artificial intelligence (AI) is intelligence—perceiving, synthesizing, and inferring information—demonstrated by machines, as opposed to intelligence displayed by non-human animals and humans. Example tasks in which this is done include speech recognition, computer vision, translation between (natural) languages, as well as other mappings of inputs.
    AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go).
    """
    summarize(sample_text)
