import google.generativeai as genai
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class BaseAgent:
    def __init__(self, model_name: str = "gemini-flash", temperature: float = 0.5):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)
        self.temperature = temperature

    def _generate_content(self, prompt: str, output_model: BaseModel):
        """Helper to generate content using the specified model and parse with Pydantic."""
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                response_mime_type="application/json",
                response_schema=output_model.model_json_schema()
            )
        )
        try:
            return output_model.model_validate_json(response.text)
        except Exception as e:
            print(f"Error parsing model output: {e}")
            print(f"Raw response text: {response.text}")
            raise