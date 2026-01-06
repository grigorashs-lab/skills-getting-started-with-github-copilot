"""
Pytest configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the varsity soccer team and compete in regional matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "james@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Play basketball and develop teamwork skills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["ryan@mergington.edu", "sarah@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore various art mediums including painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["emily@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in school plays and develop acting skills",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 30,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop critical thinking and public speaking through competitive debates",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ethan@mergington.edu", "isabella@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and participate in science competitions",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu", "charlotte@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Reset activities to original state before each test
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Cleanup after test (optional)
    activities.clear()
    activities.update(original_activities)
