from django.contrib.auth import get_user_model
import pytest
import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()


@pytest.fixture
def user_manager():
    return get_user_model().objects


@pytest.mark.django_db
def test_create_user(user_manager):
    # Test user creation with valid data
    email = 'testuser@example.com'
    password = 'TestPass123'
    user = user_manager.create_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password) is True
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_no_email(user_manager):
    # Test that creating a user without an email raises a ValueError
    with pytest.raises(ValueError) as excinfo:
        user_manager.create_user(email='', password='TestPass123')
    assert str(excinfo.value) == 'Users must have an email address'


@pytest.mark.django_db
def test_create_superuser(user_manager):
    # Test superuser creation with valid data
    email = 'superuser@example.com'
    password = 'SuperPass123'
    superuser = user_manager.create_superuser(email=email, password=password)

    assert superuser.email == email
    assert superuser.check_password(password) is True
    assert superuser.is_active is True
    assert superuser.is_staff is True
    assert superuser.is_superuser is True


@pytest.mark.django_db
def test_create_superuser_invalid_flags(user_manager):
    # Test superuser creation with invalid flags
    email = 'incomplete_superuser@example.com'
    password = 'SuperPass123'

    with pytest.raises(ValueError) as excinfo:
        user_manager.create_superuser(email=email, password=password, is_staff=False)
    assert str(excinfo.value) == 'Superuser must have is_staff=True.'

    with pytest.raises(ValueError) as excinfo:
        user_manager.create_superuser(email=email, password=password, is_superuser=False)
    assert str(excinfo.value) == 'Superuser must have is_superuser=True.'


@pytest.mark.django_db
def test_create_user_email_normalization(user_manager):
    # Test email normalization
    email = 'testuser@Example.Com'
    password = 'TestPass@123'
    user = user_manager.create_user(email=email, password=password)

    assert user.email == email.lower()
