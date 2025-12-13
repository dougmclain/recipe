#!/usr/bin/env python
"""Run this script to add the Chicken Paprikash recipe to the database."""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe, Category

user = User.objects.first()
category, _ = Category.objects.get_or_create(name='Main Course')

ingredients = '''2 lbs bone-in chicken thighs (or 1.5 lbs boneless)
2 tbsp butter
1 tbsp vegetable oil
1 large onion, diced
3 cloves garlic, minced
3 tbsp sweet Hungarian paprika
1 tsp smoked paprika (optional, for depth)
1 cup chicken broth
1 cup sour cream
1/2 cup heavy whipping cream
2 tbsp all-purpose flour
1 tsp salt
1/2 tsp black pepper
Fresh parsley, chopped (for garnish)
Egg noodles or spätzle (for serving)'''

instructions = '''Season the chicken: Pat chicken pieces dry and season generously with salt, pepper, and 1 tablespoon of the sweet paprika.
Brown the chicken: Heat butter and oil in a large Dutch oven or deep skillet over medium-high heat. Brown chicken on all sides, about 3-4 minutes per side. Remove and set aside.
Sauté the onion: Reduce heat to medium. Add diced onion to the pan and cook until soft and translucent, about 5-6 minutes. Add garlic and cook 1 minute more.
Add the paprika: Remove pan from heat briefly. Stir in the remaining sweet paprika and smoked paprika. Stir quickly to coat the onions (removing from heat prevents the paprika from burning and becoming bitter).
Build the sauce: Return to medium heat. Pour in the chicken broth, scraping up any browned bits from the bottom. Stir well to combine.
Braise the chicken: Return chicken pieces to the pan, nestling them into the sauce. Cover and simmer on low heat for 25-30 minutes until chicken is cooked through (165°F internal temperature).
Make the cream mixture: In a small bowl, whisk together the sour cream, heavy cream, and flour until smooth.
Finish the sauce: Remove chicken to a plate. Reduce heat to low. Slowly stir the cream mixture into the sauce, whisking constantly to prevent curdling. Simmer gently for 3-4 minutes until sauce thickens. Do not boil.
Combine and serve: Return chicken to the sauce and coat well. Serve over egg noodles or spätzle, garnished with fresh parsley.'''

recipe = Recipe.objects.create(
    title='Chicken Paprikash (Csirkepaprikás)',
    description='A classic Hungarian comfort dish featuring tender chicken braised in a rich, paprika-spiced cream sauce. The combination of sweet Hungarian paprika, sour cream, and heavy cream creates an incredibly silky, flavorful sauce. Traditionally served over egg noodles or spätzle.',
    ingredients=ingredients,
    instructions=instructions,
    prep_time=15,
    cook_time=45,
    servings=4,
    difficulty='easy',
    category=category,
    author=user
)

print(f'✅ Recipe created successfully! ID: {recipe.pk}, Title: {recipe.title}')
