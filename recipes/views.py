from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Recipe, Category
from .forms import RecipeForm
from .ai_image import generate_ai_image_for_recipe


class RecipeListView(ListView):
    """Display list of all recipes"""
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        queryset = Recipe.objects.all()

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(ingredients__icontains=search_query)
            )

        # Filter by category
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by difficulty
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        return context


class RecipeDetailView(DetailView):
    """Display detailed view of a single recipe"""
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Create a new recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing recipe"""
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author or self.request.user.is_superuser


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a recipe"""
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_list')

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author or self.request.user.is_superuser


def home(request):
    """Home page view"""
    recent_recipes = Recipe.objects.all()[:6]
    categories = Category.objects.all()
    context = {
        'recent_recipes': recent_recipes,
        'categories': categories,
    }
    return render(request, 'recipes/home.html', context)


@login_required
@require_http_methods(["POST"])
def generate_ai_image(request):
    """
    AJAX endpoint to generate AI image for a recipe.
    Expects POST data: title, description (optional), recipe_id (optional for updates)
    """
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    recipe_id = request.POST.get('recipe_id')
    
    if not title:
        return JsonResponse({
            'success': False,
            'error': 'Recipe title is required to generate an image.'
        }, status=400)
    
    # Check if updating existing recipe - verify ownership
    if recipe_id:
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
            if recipe.author != request.user and not request.user.is_superuser:
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied.'
                }, status=403)
        except Recipe.DoesNotExist:
            pass
    
    # Generate the AI image
    image_file, filename = generate_ai_image_for_recipe(title, description)
    
    if image_file and filename:
        # If updating existing recipe, save the image directly
        if recipe_id:
            try:
                recipe = Recipe.objects.get(pk=recipe_id)
                recipe.image.save(filename, image_file, save=True)
                return JsonResponse({
                    'success': True,
                    'message': 'AI image generated and saved successfully!',
                    'image_url': recipe.image.url if recipe.image else None
                })
            except Recipe.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Recipe not found.'
                }, status=404)
        else:
            # For new recipes, store in session temporarily
            # We'll return a data URL that the form can use
            import base64
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            return JsonResponse({
                'success': True,
                'message': 'AI image generated! Save the recipe to keep the image.',
                'image_data': f"data:image/png;base64,{image_data}",
                'filename': filename
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Failed to generate AI image. Please ensure HUGGINGFACE_API_TOKEN is set in environment variables. Get a free token at https://huggingface.co/settings/tokens'
        }, status=500)

