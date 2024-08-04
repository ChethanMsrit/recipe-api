import pytest
from recipe.models import Recipe, RecipeCategory, RecipeLike
import os
import django
from users.models import CustomUser

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()


@pytest.fixture
def user():
    return CustomUser.objects.create(username='testuser', password='Password@12356')


@pytest.fixture
def category():
    return RecipeCategory.objects.create(name='Dessert')


@pytest.fixture
def recipe(user, category):
    return Recipe.objects.create(
        author=user,
        category=category,
        picture='image_url',
        title='Chocolate Cake',
        desc='Delicious chocolate cake',
        cook_time="12:00",
        ingredients='Chocolate, flour, sugar',
        procedure='Mix and bake'
    )


@pytest.mark.django_db
def test_recipe_category_str(category):
    assert str(category) == 'Dessert'


@pytest.mark.django_db
def test_get_default_recipe_category():
    default_category = RecipeCategory.objects.get_or_create(name='Indian')
    assert default_category is not None
    assert default_category[0].name == 'Indian'


@pytest.mark.django_db
def test_recipe_str(recipe):
    assert str(recipe) == 'Chocolate Cake'


@pytest.mark.django_db
def test_get_total_number_of_likes(recipe, user):
    assert recipe.get_total_number_of_likes() == 0
    RecipeLike.objects.create(user=user, recipe=recipe)
    assert recipe.get_total_number_of_likes() == 1


@pytest.mark.django_db
def test_get_total_number_of_bookmarks(recipe, user):
    assert recipe.get_total_number_of_bookmarks() == 0
    user.profile.bookmarks.add(recipe)
    assert recipe.get_total_number_of_bookmarks() == 1


@pytest.mark.django_db
def test_recipe_like_str(recipe, user):
    recipe_like = RecipeLike.objects.create(user=user, recipe=recipe)
    assert str(recipe_like) == 'testuser'
