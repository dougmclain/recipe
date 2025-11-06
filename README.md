# Django Recipe Application

A full-featured recipe management web application built with Django. Users can create, view, edit, and delete recipes, complete with categories, difficulty levels, and image uploads.

## Features

- **Recipe Management**: Create, read, update, and delete recipes (CRUD operations)
- **User Authentication**: Login/logout functionality with user-specific recipe management
- **Recipe Details**:
  - Title, description, and instructions
  - Ingredients list
  - Preparation and cooking time
  - Servings and difficulty level
  - Recipe images
- **Categorization**: Organize recipes by categories (e.g., Dessert, Main Course, Appetizer)
- **Search & Filter**: Search recipes by keywords and filter by category or difficulty
- **Responsive Design**: Beautiful, mobile-friendly interface using Bootstrap 5
- **Admin Interface**: Django admin panel for easy content management

## Tech Stack

- **Backend**: Django 5.2+
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Image Processing**: Pillow

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd recipe
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### Adding Categories

1. Log in to the admin panel at http://127.0.0.1:8000/admin/
2. Navigate to "Categories" and click "Add Category"
3. Enter the category name and optional description
4. Save the category

### Creating Recipes

1. Log in to the main application
2. Click "Add Recipe" in the navigation bar
3. Fill in the recipe details:
   - Title and description
   - Category and difficulty level
   - Ingredients (one per line)
   - Step-by-step instructions
   - Preparation and cooking time
   - Number of servings
   - Optional recipe image
4. Click "Save Recipe"

### Browsing and Searching

- View all recipes on the "Recipes" page
- Use the search bar to find recipes by title, description, or ingredients
- Filter recipes by category or difficulty level
- Click on any recipe card to view full details

### Managing Your Recipes

- Only the recipe author (or admin) can edit or delete recipes
- Click "Edit Recipe" on the recipe detail page to modify
- Click "Delete Recipe" to remove (with confirmation)

## Project Structure

```
recipe/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── recipe_project/          # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── recipes/                 # Recipe app
    ├── __init__.py
    ├── admin.py            # Admin configuration
    ├── apps.py
    ├── forms.py            # Recipe forms
    ├── models.py           # Database models
    ├── views.py            # View logic
    ├── urls.py             # URL routing
    ├── migrations/         # Database migrations
    └── templates/
        └── recipes/        # HTML templates
            ├── base.html
            ├── home.html
            ├── recipe_list.html
            ├── recipe_detail.html
            ├── recipe_form.html
            ├── recipe_confirm_delete.html
            └── login.html
```

## Models

### Category
- `name`: Unique category name
- `description`: Optional category description
- `created_at`: Timestamp

### Recipe
- `title`: Recipe name
- `description`: Brief description
- `ingredients`: List of ingredients
- `instructions`: Cooking steps
- `prep_time`: Preparation time in minutes
- `cook_time`: Cooking time in minutes
- `servings`: Number of servings
- `difficulty`: Easy, Medium, or Hard
- `category`: Foreign key to Category
- `image`: Optional recipe image
- `author`: Foreign key to User
- `created_at` / `updated_at`: Timestamps

## Configuration

### Database

The application uses SQLite by default. To use a different database, update the `DATABASES` setting in `recipe_project/settings.py`.

### Media Files

Recipe images are stored in the `media/recipe_images/` directory. Make sure this directory is writable by the web server in production.

### Static Files

For production deployment, collect static files:
```bash
python manage.py collectstatic
```

## Development

### Running Tests

```bash
python manage.py test recipes
```

### Creating Sample Data

You can add sample recipes through the admin panel or by creating a data fixture.

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Configure static and media file serving
5. Use a production-ready web server (gunicorn, uWSGI)
6. Set up HTTPS with SSL certificate
7. Use environment variables for sensitive settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.
