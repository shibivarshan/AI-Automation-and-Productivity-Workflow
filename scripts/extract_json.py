import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import generate_json
from core.prompt_templates import EXTRACT_JSON_PROMPT
from core.validators import ExtractJsonInput
from pydantic import ValidationError

def extract_information(text: str, schema_desc: str):
    try:
        validated_input = ExtractJsonInput(
            text=text,
            schema_description=schema_desc
        )
    except ValidationError as e:
        print(f"Input Validation Error:\n{e}")
        return

    prompt = EXTRACT_JSON_PROMPT.format(
        schema=validated_input.schema_description,
        text=validated_input.text
    )
    
    print("Extracting JSON...")
    json_str = generate_json(prompt)
    
    # Try to parse it to ensure it's valid JSON
    try:
        # Strip potential markdown formatting if model didn't strictly follow JSON mime type
        if json_str.startswith("```json"):
            json_str = json_str.replace("```json", "").replace("```", "").strip()
        
        parsed_json = json.loads(json_str)
        print("\n--- Extracted JSON ---\n")
        print(json.dumps(parsed_json, indent=2))
        print("\n----------------------")
    except json.JSONDecodeError:
        print("Failed to parse the response into valid JSON. Raw output:")
        print(json_str)

if __name__ == "__main__":
    sample_text = "John Doe joined the company on October 15, 2022. He works in the Engineering department and his salary is $120,000."
    sample_schema = '{"name": "string", "join_date": "string", "department": "string", "salary": "number"}'
    
    extract_information(sample_text, sample_schema)
