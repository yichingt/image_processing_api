import pytest, io
from fastapi.testclient import TestClient
from PIL import Image

import sys, os
# Add the parent directory (where main.py is located) to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app) # Create a fake API client

#@app.post("/api/images")
def test_upload_image():
    # Create a in-memory image file for the test
    image_data = io.BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(image_data, format="JPEG")
    image_data.seek(0)

    # TO: Send POST request with image
    response = client.post(
        "/api/images",
        files={"file": ("test.jpg", image_data, "image/jpeg")}
    )

    # Assertions
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["image_status"] == "success"
    assert "image_id" in json_response["data"]
    assert "metadata" in json_response["data"]
    assert "thumbnails" in json_response["data"]
    assert "caption" in json_response["data"]

#@app.get("/api/images")
def test_get_stats():
    # Get the response from get stats
    response = client.get("/api/stats")
    assert response.status_code == 200
    json_response = response.json()
    
    assert json_response["current_status"] == "success"
    assert "success" in json_response["data"]
    assert "failure" in json_response["data"]
    assert "total_processing_time" in json_response["data"]
    assert "avg_processing_time" in json_response["data"]

#def generate_caption(image):
def test_generate_caption():
    # Create a in-memory image file for the test
    image_data = io.BytesIO()
    img = Image.new("RGB", (200, 200), color="blue")
    img.save(image_data, format="PNG")
    image_data.seek(0)

    # Send the image to the API
    response = client.post(
        "/api/images",
        files={"file": ("test.png", image_data, "image/png")}
    )

    # Assertions
    assert response.status_code == 200
    json_response = response.json()
    assert "caption" in json_response["data"]
    assert isinstance(json_response["data"]["caption"], str)

    print(f"Generated Caption: {json_response['data']['caption']}")
