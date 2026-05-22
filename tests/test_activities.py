"""Unit tests for activity management business logic using AAA pattern."""

import sys
from pathlib import Path

# Add src directory to Python path so we can import app module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import get_all_activities, signup_for_activity


class TestGetAllActivities:
    """Tests for get_all_activities() function."""

    def test_get_all_activities_returns_all_nine_activities(self, activities_db):
        """
        Test that get_all_activities returns all 9 activities.
        
        AAA Pattern:
        - Arrange: Create activities database
        - Act: Call get_all_activities
        - Assert: Verify all 9 activities are returned
        """
        # Arrange
        expected_activity_count = 9
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Swimming Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
        ]
        
        # Act
        result = get_all_activities(activities_db)
        
        # Assert
        assert len(result) == expected_activity_count
        assert list(result.keys()) == expected_activities
        assert result["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


class TestSignupForActivity:
    """Tests for signup_for_activity() function."""

    def test_signup_for_activity_success_new_email(self, activities_db):
        """
        Test successful signup for an activity with a new email.
        
        AAA Pattern:
        - Arrange: Set up activity and email
        - Act: Call signup_for_activity
        - Assert: Verify email is added and success returned
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "new_student@mergington.edu"
        initial_participant_count = len(activities_db[activity_name]["participants"])
        
        # Act
        result = signup_for_activity(activity_name, email, activities_db)
        
        # Assert
        assert result["success"] is True
        assert "Signed up" in result["message"]
        assert email in activities_db[activity_name]["participants"]
        assert len(activities_db[activity_name]["participants"]) == initial_participant_count + 1

    def test_signup_for_activity_fails_activity_not_found(self, activities_db):
        """
        Test signup fails when activity does not exist.
        
        AAA Pattern:
        - Arrange: Set up non-existent activity name and email
        - Act: Call signup_for_activity
        - Assert: Verify error returned and no participants added
        """
        # Arrange
        activity_name = "Non-Existent Activity"
        email = "student@mergington.edu"
        
        # Act
        result = signup_for_activity(activity_name, email, activities_db)
        
        # Assert
        assert result["success"] is False
        assert result["error"] == "Activity not found"

    def test_signup_for_activity_fails_duplicate_email(self, activities_db):
        """
        Test signup fails when email is already signed up for activity.
        
        AAA Pattern:
        - Arrange: Get an existing participant from an activity
        - Act: Try to sign up the same email again
        - Assert: Verify error returned and participants list unchanged
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        initial_participants = activities_db[activity_name]["participants"].copy()
        
        # Act
        result = signup_for_activity(activity_name, email, activities_db)
        
        # Assert
        assert result["success"] is False
        assert result["error"] == "Student already signed up for this activity"
        assert activities_db[activity_name]["participants"] == initial_participants

    def test_signup_for_activity_success_empty_activity(self, activities_db):
        """
        Test successful signup for an activity with no existing participants.
        
        AAA Pattern:
        - Arrange: Select an empty activity and new email
        - Act: Call signup_for_activity
        - Assert: Verify email is added to empty activity
        """
        # Arrange
        activity_name = "Swimming Club"
        email = "new_swimmer@mergington.edu"
        assert len(activities_db[activity_name]["participants"]) == 0
        
        # Act
        result = signup_for_activity(activity_name, email, activities_db)
        
        # Assert
        assert result["success"] is True
        assert len(activities_db[activity_name]["participants"]) == 1
        assert activities_db[activity_name]["participants"][0] == email
