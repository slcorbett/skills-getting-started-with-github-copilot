"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
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
    },
   "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
   "Swimming Club": {
      "description": "Swimming training and water sports",
      "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
      "max_participants": 20,
      "participants": []
   },
   "Art Studio": {
      "description": "Express creativity through painting and drawing",
      "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
      "max_participants": 15,
      "participants": []
   },
   "Drama Club": {
      "description": "Theater arts and performance training",
      "schedule": "Tuesdays, 4:00 PM - 6:00 PM",
      "max_participants": 25,
      "participants": []
   },
   "Debate Team": {
      "description": "Learn public speaking and argumentation skills",
      "schedule": "Thursdays, 3:30 PM - 5:00 PM",
      "max_participants": 16,
      "participants": []
   },
   "Science Club": {
      "description": "Hands-on experiments and scientific exploration",
      "schedule": "Fridays, 3:30 PM - 5:00 PM",
      "max_participants": 20,
      "participants": []
   }
}


# ==================== Business Logic Functions ====================

def get_all_activities(activities_db: dict) -> dict:
    """
    Retrieve all activities.
    
    Args:
        activities_db: Dictionary of activities
    
    Returns:
        Dictionary of all activities
    """
    return activities_db.copy()


def signup_for_activity(activity_name: str, email: str, activities_db: dict) -> dict:
    """
    Sign up a student for an activity.
    
    Args:
        activity_name: Name of the activity
        email: Student email
        activities_db: Dictionary of activities (mutated if successful)
    
    Returns:
        Dictionary with 'success' bool and 'message' string
    """
    # Validate activity exists
    if activity_name not in activities_db:
        return {"success": False, "error": "Activity not found"}
    
    activity = activities_db[activity_name]
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        return {"success": False, "error": "Student already signed up for this activity"}
    
    # Add student to activity
    activity["participants"].append(email)
    return {"success": True, "message": f"Signed up {email} for {activity_name}"}


# ==================== Route Handlers ====================

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return get_all_activities(activities)


@app.post("/activities/{activity_name}/signup")
def signup(activity_name: str, email: str):
    """Sign up a student for an activity"""
    result = signup_for_activity(activity_name, email, activities)
    
    if not result["success"]:
        status_code = 404 if "not found" in result["error"].lower() else 400
        raise HTTPException(status_code=status_code, detail=result["error"])
    
    return {"message": result["message"]}
