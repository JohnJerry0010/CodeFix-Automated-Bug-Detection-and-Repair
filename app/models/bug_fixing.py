import requests
import os
import logging
import time
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API Key from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# API Configuration
HF_API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-coder-1.3b-instruct"
DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def suggest_fixes(code_snippet):
    """
    Analyze Python code using Hugging Face inference API with retry mechanism.

    Args:
        code_snippet (str): Python code to analyze

    Returns:
        dict: {
            'status': 'success' or 'error',
            'fixed_code': str,
            'explanation': str,
            'message': str
        }
    """
    if not code_snippet or not isinstance(code_snippet, str):
        return {
            'status': 'error',
            'message': 'Invalid code snippet provided'
        }

    if not HF_TOKEN:
        return {
            'status': 'error',
            'message': 'API Key is missing. Set HF_TOKEN in your .env file.'
        }

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""
[INSTRUCTIONS]
You are a professional Python code assistant. 
1. Detect any bugs or issues in the code below.
2. Fix them.
3. Return:
   (a) The fixed code 
   (b) A brief explanation of what was fixed.

[CODE]
{code_snippet}
"""

    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                HF_API_URL,
                headers=headers,
                json=payload,
                timeout=DEFAULT_TIMEOUT
            )

            if response.status_code == 200:
                result = response.json()

                # Some models return a list with a 'generated_text' key
                generated_text = result[0].get('generated_text', '')

                # Basic extraction from expected response pattern
                explanation_split = generated_text.split("Explanation:")
                fixed_code = explanation_split[0].strip().replace("[FIXED CODE]", "").strip()
                explanation = explanation_split[1].strip() if len(explanation_split) > 1 else "Explanation not provided."

                return {
                    'status': 'success',
                    'fixed_code': fixed_code,
                    'explanation': explanation,
                    'message': 'Fix generated successfully.'
                }

            else:
                logger.warning(f"[Attempt {attempt}] Request failed: {response.status_code} - {response.text}")
                time.sleep(RETRY_DELAY)

        except requests.exceptions.RequestException as e:
            logger.error(f"[Attempt {attempt}] Exception occurred: {e}")
            time.sleep(RETRY_DELAY)

    return {
        'status': 'error',
        'message': 'Failed to retrieve fix after multiple attempts.'
    }
