import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API client
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("Warning: OPENAI_API_KEY not found in .env file.")

# Initialize the client
try:
    client = OpenAI(api_key=API_KEY) if API_KEY else None
except Exception as e:
    print(f"Failed to initialize client: {e}")
    client = None

def generate_text(prompt: str) -> str:
    """Generates text from a given prompt using OpenAI."""
    if not client:
        return "Error: Client not initialized (check API key)."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating text: {str(e)}"

def generate_json(prompt: str) -> str:
    """
    Generates text ensuring the output is valid JSON using OpenAI JSON mode.
    """
    if not client:
        return '{"error": "Client not initialized (check API key)."}'
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f'{{"error": "Error generating JSON: {str(e)}"}}'
