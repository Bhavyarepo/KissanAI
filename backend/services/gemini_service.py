from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    async def get_farming_advice(self, question: str, context: str = ""):
        if not self.client:
            return "Gemini API key is not configured. Please set GOOGLE_API_KEY in the .env file."
        
        prompt = f"""
        You are an expert agricultural advisor. 
        Context information: {context}
        
        User Question: {question}
        
        Provide detailed, scientific, and practical agricultural advice. 
        If the user asks for crop recommendations, consider the local climate and soil conditions if provided in context.
        Keep the response helpful for a farmer.
        """
        
        try:
            # Using the new google-genai SDK
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"

    async def get_enhanced_recommendations(self, crop: str, soil: dict, weather: dict):
        if not self.client:
            return None
        
        prompt = f"""
        Provide detailed cultivation advice for {crop} based on:
        Soil: {soil}
        Weather: {weather}
        
        Include:
        1. Sowing depth and spacing
        2. Fertilizer application schedule
        3. Potential risks and mitigation
        4. Expected yield optimization tips
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text
        except Exception:
            return None
    async def is_image_a_crop(self, image_path: str):
        if not self.client:
            return True, "Skipping validation as Gemini is not configured."
        
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # Using Gemini 1.5 Flash (or 2.0/2.5) for vision
            response = self.client.models.generate_content(
                model='gemini-2.0-flash', # Use 2.0 as it's reliable for vision
                contents=[
                    "Is this image a picture of a crop, plant, leaf, or agricultural field? Answer with 'YES' or 'NO' and a short reason.",
                    {'mime_type': 'image/jpeg', 'data': image_data}
                ]
            )
            
            text = response.text.upper()
            if "YES" in text:
                return True, "Image validated as a crop."
            else:
                return False, "The uploaded image is not a plant or crop. Please upload a clear image of your crop for detection."
        except Exception as e:
            return True, f"Error validating image (defaulting to True): {str(e)}"
