# Django Recipe Application - AI Coding Agent Instructions

## Project Overview
Django 5.2 recipe management application with user authentication, CRUD operations, AI-powered image generation, and search/filter capabilities. Single-app architecture (`recipes`) within `recipe_project`.

## Architecture & Structure

### App Organization
- **`recipes/`**: Single Django app containing all models, views, forms, and templates
- **`recipe_project/`**: Main Django project with settings, URLs, and WSGI/ASGI config
- **Models**: `Recipe` and `Category` in `recipes/models.py`
  - Recipes have `author` (User FK), `category` (FK), difficulty choices, and image uploads
  - Category uses `SET_NULL` on delete to preserve recipes when categories removed
- **AI Integration**: `recipes/ai_image.py` handles AI image generation via Hugging Face API

### URL Routing Pattern
Two-level URL configuration:
1. `recipe_project/urls.py`: Includes `recipes.urls` at root path + auth views + admin
2. `recipes/urls.py`: All recipe-specific URLs (home, list, detail, CRUD)
3. Media files served via `static()` in development only (check `settings.DEBUG`)

### Authentication Flow
- Uses Django's built-in `auth_views.LoginView` with custom template at `recipes/login.html`
- Login redirects configured via `LOGIN_REDIRECT_URL = 'home'` in settings
- Views use `LoginRequiredMixin` for auth and `UserPassesTestMixin` for ownership checks
- Recipe create/update/delete restricted to recipe author or superuser

## Development Workflow

### Running the Application
```bash
python manage.py runserver  # Starts on http://127.0.0.1:8000/
```

### Database Operations
```bash
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin user
```

### Key Commands
- Access admin panel at `/admin/` to manage categories (users must create categories via admin before recipes can use them)
- Media files stored in `media/recipe_images/` (created automatically via `upload_to`)

## Coding Conventions

### Class-Based Views (CBV) Pattern
All recipe views use Django generic CBVs (`ListView`, `DetailView`, `CreateView`, etc.) in `recipes/views.py`:
- Override `get_queryset()` for search/filter logic (see `RecipeListView`)
- Override `get_context_data()` to add categories and filter state to templates
- Override `form_valid()` to set current user as author on create
- Override `test_func()` for permission checks (author or superuser)

### Form Handling
`RecipeForm` (ModelForm) uses extensive widget customization with Bootstrap classes:
- All form fields have `class: 'form-control'` and contextual placeholders
- Form rendered in templates using `{{ form.as_p }}` or manual field rendering

### Template Organization
- Base template: `recipes/templates/recipes/base.html` with Bootstrap 5 + Bootstrap Icons
- Template inheritance: All templates extend `base.html` and override `{% block title %}` and `{% block content %}`
- Custom CSS variables: `--primary-color: #ff6b6b`, `--secondary-color: #4ecdc4`
- Print styles included for PDF generation from recipe detail pages

### Query Patterns
Search uses `Q` objects for OR queries across title/description/ingredients:
```python
queryset.filter(
    Q(title__icontains=search_query) |
    Q(description__icontains=search_query) |
    Q(ingredients__icontains=search_query)
)
```

## Important Details

### Static & Media Files
- `STATIC_URL = "static/"`, `STATIC_ROOT = BASE_DIR / "staticfiles"`
- `MEDIA_URL = "media/"`, `MEDIA_ROOT = BASE_DIR / "media"`
- Media files only served in development (requires `settings.DEBUG = True`)

### Model Properties
- `Recipe.total_time` computed property returns `prep_time + cook_time`
- `get_absolute_url()` points to `recipe_detail` view

### Admin Configuration
Admin classes use `@admin.register()` decorator with:
- `list_display` for table columns
- `list_filter` for sidebar filtering
- `fieldsets` for organized form layout (see `RecipeAdmin`)
- `readonly_fields` for timestamps

### Dependencies
- **Django**: Version constraint `>=4.2,<5.0` in `requirements.txt` (but settings show Django 5.2.8 in use - version mismatch)
- **Pillow**: Required for image upload handling
- **requests**: HTTP library for Hugging Face API calls
- **python-dotenv**: Load environment variables from `.env` file

### Environment Variables
Project uses `.env` file for sensitive configuration (loaded via `python-dotenv` in `settings.py`):
- `HUGGINGFACE_API_TOKEN`: Required for AI image generation (get free token at https://huggingface.co/settings/tokens)
- See `.env.example` for template

## AI Image Generation Feature

### Architecture
- **Module**: `recipes/ai_image.py` contains `AIImageGenerator` class
- **API**: Hugging Face Inference API with Stable Diffusion 2.1 (free tier)
- **Endpoint**: `/recipe/generate-ai-image/` (POST) in `recipes/views.py`
- **UI**: AJAX-powered button in `recipe_form.html` with loading states

### Workflow
1. User clicks "Generate AI Image" button in recipe form
2. JavaScript POSTs title/description to `/recipe/generate-ai-image/`
3. Backend creates food photography prompt from recipe details
4. Calls Hugging Face API (may take 10-30 seconds, especially first time)
5. For **existing recipes**: Image saved directly to model, returns URL
6. For **new recipes**: Returns base64 data URL for preview (saved on form submit)
7. UI shows loading spinner, then preview or error message

### Key Implementation Details
- Permission check: Only recipe author or superuser can generate images
- Error handling: Returns JSON with `success: false` if API token missing or API fails
- Image format: Converted to PNG via Pillow before saving
- Prompt engineering: Adds "professional food photography, beautifully plated, high quality" to recipe title

### Adding AI to Other Features
When adding AI image generation to other parts of the app:
1. Import `generate_ai_image_for_recipe()` from `recipes.ai_image`
2. Call with recipe title and optional description
3. Returns tuple: `(ContentFile, filename)` or `(None, None)` on failure
4. Save ContentFile to model's ImageField: `recipe.image.save(filename, content_file, save=True)`

## Common Tasks

### Adding New Recipe Fields
1. Add field to `Recipe` model in `models.py`
2. Update `RecipeForm.Meta.fields` and add widget in `forms.py`
3. Run `makemigrations` and `migrate`
4. Update `RecipeAdmin.list_display` or fieldsets if needed
5. Update templates to display new field

### Adding Authentication to New Views
Use mixins: `LoginRequiredMixin` for login requirement, `UserPassesTestMixin` with `test_func()` for permission checks.
