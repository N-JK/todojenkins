import pytest
from django.urls import reverse
from django.test import Client
from base.models import Task
from django.contrib.auth.models import User

# This pytest uses Django's TestClient to simulate requests and test views

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    # Create a test user for authentication in view tests
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def task():
    # Create a test Task instance for model tests
    return Task.objects.create(title="Test Task", description="This is a test task.")

# Testing the models
@pytest.mark.django_db
def test_task_model(task):
    # Test that the Task model saves correctly
    assert task.title == "Test Task"
    assert task.description == "This is a test task."
