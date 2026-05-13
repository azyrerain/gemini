import google.genai as genai

class GeminiClient:
    def __init__(self, api_key: str, model: str = None):
        self.client = genai.Client(api_key=api_key)
        if model:
            self.model = model
        else:
            # pick the first "pro" model available
            models = [m.name for m in self.client.models.list() if "pro" in m.name]
            self.model = models[0] if models else None

    def get_response(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt   # plain string works for text prompts
        )
        return response.text

    def list_models(self):
        # Returns all model names available to your account
        return [m.name for m in self.client.models.list()]
