import os
from google import genai

class RootAgent:
    def __init__(self, system_prompt: str):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable not set")

        self.client = genai.Client(api_key=api_key)
        self.system_prompt = system_prompt
        self.model = "gemini-1.5-flash"

    def run(self, user_input: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            config=genai.types.GenerateContentConfig(
                system_instruction=self.system_prompt
            ),
            contents=user_input
        )

        return response.text