import google.genai as genai
import time, random

class GeminiClient:
    FREE_MODELS = [
        "models/gemini-3.1-flash-lite",
        "models/gemini-2.5-flash-lite",
        "models/gemini-2.0-flash-lite",
        "models/gemini-flash-lite-latest",
    ]

    def __init__(self, api_key: str, model: str = None):
        self.client = genai.Client(api_key=api_key)
        # Default to the first free model if none specified
        self.model = model or self.FREE_MODELS[0]

    def get_response(self, prompt: str) -> str:
        # Try each free model in sequence
        for model in self.FREE_MODELS:
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                return response.text
            except genai.errors.ClientError as e:
                # Retry with backoff if it's a temporary overload
                if "UNAVAILABLE" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(1 + random.random())
                    continue
                raise
        return "All free models are currently overloaded. Please try again later."

    def list_models(self):
        return [m.name for m in self.client.models.list()]
