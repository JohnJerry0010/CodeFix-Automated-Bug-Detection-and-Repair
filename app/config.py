from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Define the model name
MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

# ✅ Load model and tokenizer ONCE
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

# ✅ Function to generate responses
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
