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

# Testing the views
@pytest.mark.django_db
def test_home_view(client, user):
    client.login(username='testuser', password='testpass')
    url = reverse('home')  # Assuming the URL name for the home view is 'home'
    response = client.get(url)
    
    # Ensure that the response is 200 OK
    assert response.status_code == 200
    # Ensure that the correct template is used
    assert 'base/home.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_task_detail_view(client, task, user):
    client.login(username='testuser', password='testpass')
    url = reverse('task-detail', args=[task.id])  # Assuming URL pattern for task detail uses the task id
    response = client.get(url)

    # Ensure that the response is 200 OK
    assert response.status_code == 200
    # Ensure the task title is in the response content
    assert task.title in response.content.decode()

# Testing URL routing
@pytest.mark.django_db
def test_urls(client):
    # Test that the URL for the home view resolves correctly
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200

    # Test that the URL for a task's detail page resolves correctly
    task = Task.objects.create(title="Test Task", description="Testing URL resolution.")
    url = reverse('task-detail', args=[task.id])
    response = client.get(url)
    assert response.status_code == 200
