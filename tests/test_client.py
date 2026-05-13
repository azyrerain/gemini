import pytest
from gemini import GeminiClient

def test_client_init():
    client = GeminiClient(api_key="dummy")
    assert client.model == "gemini-1.5-flash"
