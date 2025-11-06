from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    """Form for creating and updating recipes"""

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions',
                  'prep_time', 'cook_time', 'servings', 'difficulty', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter recipe title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief description of the recipe'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'List ingredients (one per line)'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Step-by-step cooking instructions'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Minutes'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of servings'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
