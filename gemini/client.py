import google.genai as genai

class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[{"role": "user", "parts": [prompt]}]
        )
        return response.text
