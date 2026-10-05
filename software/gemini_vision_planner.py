"""
Desktop AI Robot Arm - Gemini Vision Planner Script
====================================================
Uses Google's Gemini 2.0 Flash API to act as the "Visual Brain" for the robot arm.
It inspects an image of the workspace (from a simulator camera or webcam)
and outputs structured JSON with the normalized target coordinates [x, y, z].

Setup:
1. pip install google-genai pillow pydantic
2. export GEMINI_API_KEY="your-api-key" (from https://aistudio.google.com)
"""

import os
import json
from google import genai
from google.genai import types
from PIL import Image

def get_target_coordinates_from_image(image_path: str, user_instruction: str = "Pick up the red cube"):
    """
    Sends workspace camera frame to Gemini 2.0 Flash to locate target object coordinates.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY environment variable not set. Set it before calling the API.")
        return None

    client = genai.Client(api_key=api_key)
    
    # Open image from path
    image = Image.open(image_path)
    
    prompt = f"""
    You are the robotic vision planner for a desktop 6-DOF robotic manipulator arm.
    Goal: "{user_instruction}"
    
    Analyze the table workspace in this camera view.
    Find the target object.
    Output a strictly formatted JSON object with normalized coordinates (0.0 to 1.0)
    where (0,0) is top-left and (1,1) is bottom-right:
    {{
        "target_detected": true,
        "object_name": "red cube",
        "x_norm": 0.52,
        "y_norm": 0.64,
        "depth_level": "table_surface",
        "approach_angle_degrees": 0.0,
        "gripper_action": "open_then_grasp"
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, image],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    result = json.loads(response.text)
    return result

if __name__ == "__main__":
    print("Gemini Vision Planner module ready.")
    print("To test: provide a workspace photo or simulated camera frame.")
