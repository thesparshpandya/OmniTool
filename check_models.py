# This just prints names of available models in the API you are using
import os
from google import genai

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

print("✅ AVAILABLE MODELS:")
try:
    for m in client.models.list():
        # Just print the name, don't try to access other properties
        print(f" - {m.name.replace('models/', '')}")
except Exception as e:
    print(f"Error: {e}")
