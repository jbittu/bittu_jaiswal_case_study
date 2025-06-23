import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
from abc import ABC, abstractmethod
import os

class BaseAgent(ABC):
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def _generate_content(self, prompt: str, output_model: type[BaseModel]) -> BaseModel:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return output_model.model_validate_json(response.text)
        except Exception as e:
            print(f"Error during content generation or parsing in BaseAgent: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                print(f"Raw model response text: {response.text}")
            if 'response' in locals() and hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                print(f"Prompt feedback: {response.prompt_feedback}")
            raise
