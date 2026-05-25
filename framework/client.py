import base64
from urllib.parse import urljoin

import requests
import os
import pathlib
import re
import json
from config import settings



class OllamaClient:
    def __init__(self, model:str):
        self.base_url = settings.OLLAMA_API_BASE_URL
        self.model = settings.VLM_MODEL_NAME

    def get_model(self):
        return self.model

    def call_image_model(self, image: base64 , question: str) ->  dict:

        payload = {
            "model": self.model,  # Use the stored model name
            "prompt": (
                f"{question}\n\n"
                'Return ONLY valid JSON in this exact format:\n'
                '{"Description": "", "Probability": 1.0}'),
            "images": [image],
            "stream": False,          # False = wait for complete response
            "options": {
                "temperature": 0.1    # low = consistent responses
            }
        }

        try:
            full_url = urljoin(self.base_url, settings.ENDPOINT_GENERATE)
            response = requests.post(full_url,
                                     json=payload,
                                     timeout=300)
            response.raise_for_status()
            raw_data = response.json()
            # Extract the raw response string
            raw_text = raw_data.get("response", "")

            # Clean up potential Markdown formatting
            cleaned_text = re.sub(r'```json|```', '', raw_text).strip()

            # Parse into a dictionary
            return json.loads(cleaned_text)

        except requests.exceptions.Timeout:
            print("ERROR: Request timed out.")
            print("FIX: Model may still be loading. Wait 30s and try again.")
            return None

        except requests.exceptions.HTTPError as e:
            print(f"ERROR: API returned error: {e}")
            return None

        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")
            return None

    def call_text_model(self, question: str) -> dict:
        # print("Granite Launched")
        payload = {
            "model": self.model,  # Use the stored model name
            "prompt": (

                f"{question}\n\n"
                'Return ONLY valid JSON in this exact format:\n'
                '{"Description": "", "Probability": 1.0}'),
            "stream": False,  # False = wait for complete response
            "options": {
                "temperature": 0.1  # low = consistent responses
            }
        }

        try:
            full_url = urljoin(self.base_url, settings.ENDPOINT_GENERATE)
            response = requests.post(full_url,
                                     json=payload,
                                     timeout=300)
            response.raise_for_status()
            raw_data = response.json()
            # Extract the raw response string
            raw_text = raw_data.get("response", "")

            # Clean up potential Markdown formatting
            cleaned_text = re.sub(r'```json|```', '', raw_text).strip()

            # Parse into a dictionary
            return json.loads(cleaned_text)

        except requests.exceptions.Timeout:
            print("ERROR: Request timed out.")
            print("FIX: Model may still be loading. Wait 30s and try again.")
            return None

        except requests.exceptions.HTTPError as e:
            print(f"ERROR: API returned error: {e}")
            return None

        except Exception as e:
            print(f"ERROR: Unexpected error: {e}")
            return None



# Load image
#with open(".../image-testing-framework/test_images/ghibli.png", "rb") as f:
 #   image_b64 = base64.b64encode(f.read()).decode("utf-8")

# Create one client
#client = OllamaClient(model="llava:7b")

# Use it multiple times
#response1 = client.call_image_model(image_b64, "Is this a cartoon?")

#print(response1)
