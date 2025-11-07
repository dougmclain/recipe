import requests
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
import os


class AIImageGenerator:
    """
    Generate AI images using Hugging Face's free Inference API.
    Falls back to placeholder if API fails or no token provided.
    """
    
    # Free models available on Hugging Face
    DEFAULT_MODEL = "stabilityai/stable-diffusion-2-1"
    
    def __init__(self):
        self.api_token = os.environ.get('HUGGINGFACE_API_TOKEN', '')
        self.api_url = f"https://api-inference.huggingface.co/models/{self.DEFAULT_MODEL}"
    
    def generate_recipe_image(self, recipe_title, recipe_description=""):
        """
        Generate an AI image for a recipe.
        
        Args:
            recipe_title: The title of the recipe
            recipe_description: Optional description for more context
            
        Returns:
            tuple: (ContentFile object, filename) or (None, None) if failed
        """
        if not self.api_token:
            return None, None
        
        # Create a food photography prompt
        prompt = self._create_prompt(recipe_title, recipe_description)
        
        try:
            image_bytes = self._call_api(prompt)
            if image_bytes:
                # Convert to PIL Image to ensure it's valid
                img = Image.open(io.BytesIO(image_bytes))
                
                # Save to BytesIO
                img_io = io.BytesIO()
                img.save(img_io, format='PNG')
                img_io.seek(0)
                
                # Create filename from recipe title
                filename = f"ai_{recipe_title[:30].replace(' ', '_').lower()}.png"
                
                return ContentFile(img_io.read()), filename
            
        except Exception as e:
            print(f"AI Image generation error: {e}")
            return None, None
        
        return None, None
    
    def _create_prompt(self, recipe_title, recipe_description):
        """Create an optimized prompt for food photography"""
        base_prompt = f"Professional food photography of {recipe_title}, "
        base_prompt += "beautifully plated, high quality, appetizing, "
        base_prompt += "natural lighting, restaurant quality, detailed, 8k"
        
        return base_prompt
    
    def _call_api(self, prompt, max_retries=3):
        """
        Call Hugging Face Inference API.
        
        Args:
            prompt: Text prompt for image generation
            max_retries: Number of retries if model is loading
            
        Returns:
            bytes: Image data or None if failed
        """
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": prompt}
        
        for attempt in range(max_retries):
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.content
            elif response.status_code == 503:
                # Model is loading, wait and retry
                import time
                time.sleep(10)
                continue
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        
        return None


def generate_ai_image_for_recipe(recipe_title, recipe_description=""):
    """
    Helper function to generate AI image for a recipe.
    
    Returns:
        tuple: (ContentFile, filename) or (None, None)
    """
    generator = AIImageGenerator()
    return generator.generate_recipe_image(recipe_title, recipe_description)
