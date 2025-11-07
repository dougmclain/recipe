# AI Image Generation Setup

## Overview
Your Django Recipe App now has AI-powered image generation! Users can click a button to generate professional food photography for their recipes using Hugging Face's free Stable Diffusion API.

## Features Added
- ✨ **Generate AI Images**: Click "Generate AI Image" button in recipe forms
- 🎨 **Smart Prompts**: Automatically creates food photography prompts from recipe titles
- 💾 **Seamless Integration**: Images save directly to existing recipes or preview for new recipes
- 🆓 **Free to Use**: Uses Hugging Face's free inference API

## Setup Instructions

### 1. Get a Free Hugging Face API Token
1. Go to [https://huggingface.co/](https://huggingface.co/)
2. Sign up for a free account (or log in)
3. Go to Settings → Access Tokens: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
4. Click "New token"
5. Give it a name (e.g., "Recipe App") and select "Read" permission
6. Copy the generated token

### 2. Configure Environment Variables
1. Create a `.env` file in your project root:
   ```bash
   cd /Users/Doug/Projects/Recipe_program/recipe
   cp .env.example .env
   ```

2. Edit `.env` and add your Hugging Face token:
   ```
   HUGGINGFACE_API_TOKEN=hf_your_actual_token_here
   ```

### 3. Run Migrations (if needed)
```bash
python manage.py migrate
```

### 4. Start the Server
```bash
python manage.py runserver
```

## How to Use

### For New Recipes:
1. Go to "Add Recipe"
2. Enter the recipe title (required)
3. Optionally add a description for better results
4. Click "Generate AI Image" button
5. Wait 10-30 seconds (first generation may take longer)
6. Preview the generated image
7. Save the recipe

### For Existing Recipes:
1. Go to any recipe you authored
2. Click "Edit"
3. Click "Generate AI Image" button
4. The image will be automatically saved to the recipe
5. Save to confirm changes

## Technical Details

### Files Modified/Added:
- `recipes/ai_image.py` - AI image generation logic
- `recipes/views.py` - Added AJAX endpoint for image generation
- `recipes/urls.py` - Added route for AI image generation
- `recipes/templates/recipes/recipe_form.html` - Added UI with button and loading states
- `requirements.txt` - Added requests and python-dotenv
- `recipe_project/settings.py` - Added dotenv support
- `.env.example` - Template for environment variables

### How It Works:
1. User clicks "Generate AI Image" button
2. JavaScript sends AJAX POST request with recipe title/description
3. Backend creates optimized food photography prompt
4. Calls Hugging Face Stable Diffusion 2.1 API
5. Receives image, converts to PNG
6. For existing recipes: Saves directly to database
7. For new recipes: Returns base64 preview (saved on form submit)

### API Limits:
- Hugging Face free tier has rate limits
- First request may take 20-30 seconds (model loading)
- Subsequent requests are faster (~10 seconds)
- If you exceed limits, upgrade to Hugging Face Pro ($9/month)

### Troubleshooting:

**"Failed to generate AI image" error:**
- Check that `HUGGINGFACE_API_TOKEN` is set in `.env`
- Verify token is valid at [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Check terminal for detailed error messages

**Image generation is slow:**
- First request loads the model (20-30 seconds)
- Subsequent requests are faster
- This is normal for free tier

**Button doesn't work:**
- Make sure you entered a recipe title first
- Check browser console for JavaScript errors
- Ensure you're logged in

## Future Enhancements
- Allow users to regenerate with different styles
- Add prompt customization options
- Support multiple image models
- Batch generation for multiple recipes

## Need Help?
Check the terminal output for detailed error messages when generating images.
