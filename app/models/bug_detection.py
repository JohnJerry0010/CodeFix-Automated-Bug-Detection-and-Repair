

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ddexterr/Bug-Classification")
model = AutoModelForSequenceClassification.from_pretrained("ddexterr/Bug-Classification")

def detect_bug(code_snippet):
    """
    Analyze Python code for bugs using the pre-trained binary classification model.
    
    Args:
        code_snippet (str): Python code to analyze
        
    Returns:
        dict: {
            'status': 'Bug-Free' or 'Bug Detected',
            'confidence': float,
            'message': str
        }
    """
    if not code_snippet or not isinstance(code_snippet, str):
        return {
            'status': 'Error',
            'confidence': 0.0,
            'message': 'Invalid code snippet provided'
        }

    try:
        # Tokenize the input
        inputs = tokenizer(
            code_snippet,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # Get model prediction
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Process output (binary classification)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][predicted_class].item()
        
        # Return results
        if predicted_class == 1:  # Assuming 1 is the "Buggy" class
            return {
                'status': 'Bug Detected',
                'confidence': confidence,
                'message': 'Potential bugs found in the code'
            }
        else:
            return {
                'status': 'Bug-Free',
                'confidence': confidence,
                'message': 'No bugs detected in the code'
            }
            
    except Exception as e:
        logger.error(f"Error during bug detection: {str(e)}")
        return {
            'status': 'Error',
            'confidence': 0.0,
            'message': f'Failed to analyze code: {str(e)}'
        }