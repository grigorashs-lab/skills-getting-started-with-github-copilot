"""
Tests for the activities endpoints
"""
import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_success(self, client):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Soccer Team" in data
        assert "Programming Class" in data
        
    def test_activities_structure(self, client):
        """Test that activities have correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, details in data.items():
            assert "description" in details
            assert "schedule" in details
            assert "max_participants" in details
            assert "participants" in details
            assert isinstance(details["participants"], list)
            assert isinstance(details["max_participants"], int)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify student was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate(self, client):
        """Test signing up when already registered"""
        # First signup
        client.post("/activities/Chess Club/signup?email=test@mergington.edu")
        
        # Try to signup again
        response = client.post(
            "/activities/Chess Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_nonexistent_activity(self, client):
        """Test signing up for a non-existent activity"""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()
    
    def test_signup_with_special_characters_in_name(self, client):
        """Test signing up for activity with special characters"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=test@mergington.edu"
        )
        assert response.status_code == 200


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client):
        """Test successful unregistration from an activity"""
        # First, sign up a student
        client.post("/activities/Chess Club/signup?email=test@mergington.edu")
        
        # Then unregister
        response = client.delete(
            "/activities/Chess Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert "test@mergington.edu" in data["message"]
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "test@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_existing_participant(self, client):
        """Test unregistering an existing participant"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_not_signed_up(self, client):
        """Test unregistering when not signed up"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        
        data = response.json()
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity(self, client):
        """Test unregistering from a non-existent activity"""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=test@mergington.edu"
        )
        assert response.status_code == 404
        
        data = response.json()
        assert "not found" in data["detail"].lower()


class TestRootEndpoint:
    """Tests for GET / endpoint"""
    
    def test_root_redirect(self, client):
        """Test that root redirects to static index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestIntegrationScenarios:
    """Integration tests for complete user scenarios"""
    
    def test_signup_and_unregister_flow(self, client):
        """Test complete flow of signing up and unregistering"""
        email = "integration@mergington.edu"
        activity = "Programming Class"
        
        # Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()[activity]["participants"])
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Verify added
        response = client.get("/activities")
        assert len(response.json()[activity]["participants"]) == initial_count + 1
        assert email in response.json()[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify removed
        response = client.get("/activities")
        assert len(response.json()[activity]["participants"]) == initial_count
        assert email not in response.json()[activity]["participants"]
    
    def test_multiple_signups_different_activities(self, client):
        """Test signing up for multiple activities"""
        email = "multisport@mergington.edu"
        
        # Sign up for multiple activities
        activities = ["Chess Club", "Programming Class", "Science Club"]
        
        for activity in activities:
            response = client.post(
                f"/activities/{activity}/signup?email={email}"
            )
            assert response.status_code == 200
        
        # Verify all signups
        response = client.get("/activities")
        data = response.json()
        
        for activity in activities:
            assert email in data[activity]["participants"]
