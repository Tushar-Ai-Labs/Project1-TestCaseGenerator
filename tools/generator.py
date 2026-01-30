import requests
import json
import logging

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:4b"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a QA Automation Expert. Your task is to generate comprehensive test cases based on the user's feature description.
You must output ONLY valid JSON.
The JSON structure must be:
{
  "test_cases": [
    {
      "id": "TC_XXX",
      "title": "Title of the test",
      "description": "Brief description",
      "preconditions": "Preconditions if any",
      "steps": ["Step 1", "Step 2"],
      "expected_result": "Expected outcome"
    }
  ]
}
Do not add any markdown formatting (like ```json), just the raw JSON string.
"""

def generate_test_cases(feature_description, test_type="all"):
    """
    Generates test cases from a feature description using Ollama.
    Returns a dictionary (parsed JSON).
    """
    type_instruction = ""
    if test_type == "positive":
        type_instruction = "Generate ONLY POSITIVE test cases (happy paths)."
    elif test_type == "negative":
        type_instruction = "Generate ONLY NEGATIVE test cases (edge cases, error conditions, invalid inputs)."
    else:
        type_instruction = "Generate a mix of POSITIVE and NEGATIVE test cases."

    prompt = f"Feature Description: {feature_description}\n\nInstruction: {type_instruction}\n\nGenerate test cases in JSON format."
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": True,
        "options": {
            "temperature": 0.2
        }
    }
    
    logger.info(f"Sending request to Ollama ({MODEL})...")
    
    try:
        # Use stream=True and accumulate the response
        full_response = ""
        with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=300) as response:
            try:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if "response" in data:
                            full_response += data["response"]
                        if data.get("done") is True:
                            break
            except requests.exceptions.RequestException as e:
                # If we got some data, maybe we can still use it? No, JSON would be incomplete.
                logger.error(f"Stream interrupted: {e}")
                raise
                
        raw_text = full_response.strip()
        logger.info(f"Ollama response received. Length: {len(raw_text)}")
        
        # Cleanup potential markdown code blocks
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1)
        if raw_text.startswith("```"):
             raw_text = raw_text.replace("```", "", 1)
        if raw_text.endswith("```"):
             raw_text = raw_text.rsplit("```", 1)[0]
             
        parsed_json = json.loads(raw_text)
        return parsed_json
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API Error: {e}")
        raise Exception(f"Failed to connect to LLM: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON Parse Error: {e}. Raw Text: {raw_text}")
        raise Exception(f"LLM returned invalid JSON. Raw text: {raw_text[:100]}...")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        raise

if __name__ == "__main__":
    # Test run
    sample = "Login page with email and password fields."
    print(json.dumps(generate_test_cases(sample), indent=2))
