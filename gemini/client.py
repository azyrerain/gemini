import google.genai as genai

class GeminiClient:
    def __init__(self, api_key: str, model: str = "models/gemini-1.5-pro"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text
        
    def list_models(self):
        # Returns all model names available to your account
        return [m.name for m in self.client.models.list()]
