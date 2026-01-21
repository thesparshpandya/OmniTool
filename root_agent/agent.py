import os
import google.generativeai as genai

class RootAgent:
    def __init__(self, system_prompt: str):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable not set")

        genai.configure(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def run(self, user_input: str) -> str:
        response = self.model.generate_content(
            [
                {"role": "system", "parts": [self.system_prompt]},
                {"role": "user", "parts": [user_input]},
            ]
        )
        return response.text