import io
from PIL import Image
from django.core.files.base import ContentFile
from django.conf import settings
import os
from pathlib import Path
from dotenv import load_dotenv

# Ensure .env is loaded
load_dotenv(Path(__file__).resolve().parent.parent / '.env')


class AIImageGenerator:
    """
    Generate AI images using Hugging Face's Inference Providers.
    Falls back to placeholder if API fails or no token provided.
    """
    
    # Free model available on Hugging Face
    DEFAULT_MODEL = "black-forest-labs/FLUX.1-dev"
    
    def __init__(self):
        self.api_token = os.environ.get('HUGGINGFACE_API_TOKEN', '')
        if not self.api_token:
            print("WARNING: HUGGINGFACE_API_TOKEN not found in environment")
    
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
        Call Hugging Face Inference API using huggingface_hub library.
        
        Args:
            prompt: Text prompt for image generation
            max_retries: Number of retries if model is loading
            
        Returns:
            bytes: Image data or None if failed
        """
        try:
            from huggingface_hub import InferenceClient
            
            client = InferenceClient(token=self.api_token)
            
            for attempt in range(max_retries):
                try:
                    # Generate image using the new API
                    image = client.text_to_image(
                        prompt=prompt,
                        model=self.DEFAULT_MODEL
                    )
                    
                    # Convert PIL Image to bytes
                    img_io = io.BytesIO()
                    image.save(img_io, format='PNG')
                    img_io.seek(0)
                    return img_io.read()
                    
                except Exception as e:
                    error_str = str(e).lower()
                    if 'loading' in error_str or '503' in error_str:
                        # Model is loading, wait and retry
                        import time
                        print(f"Model loading, waiting... (attempt {attempt + 1})")
                        time.sleep(10)
                        continue
                    else:
                        print(f"API Error: {e}")
                        return None
                        
        except ImportError:
            print("huggingface_hub not installed. Run: pip install huggingface_hub")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
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
