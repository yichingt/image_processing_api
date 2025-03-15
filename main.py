from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
import io, os, uuid, time
from datetime import datetime
import uvicorn
from transformers import BlipProcessor, BlipForConditionalGeneration

app = FastAPI()

# https://huggingface.co/Salesforce/blip-image-captioning-base
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Storing results in memory, processed_results_stats for /api/stats
processed_results = {}
processed_results_stats = {"success": 0, "failure": 0, "total_processing_time": 0, "avg_processing_time": 0}

# Functions
def extract_metadata(image, file_path):
  # Extract basic metadata (dimensions, format, size), dimension -> width and height
  return {
      "width": image.width,
      "height": image.height,
      "format": image.format.upper(),
      "size_bytes": os.path.getsize(file_path),
      "created_at": datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S"),
      "modified_at": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
  }

def generate_thumbnails(image, image_id: str, file_extension: str):
  # Generate thumbnails (2 different sizes) 
  # example given: "small": "http://localhost:8000/api/images/img123/thumbnails/small" and "medium": "http://localhost:8000/api/images/img123/thumbnails/medium"
  
  thumbnails = {}
  #small_tn = image.resize((128, 128))
  #medium_tn = image.resize((512, 512))
  sizes = {
      "small": (128, 128),
      "medium": (512, 512)
  }
  
  # Create directory
  tn_dir = f"{image_id}/thumbnails"
  os.makedirs(f"{image_id}/thumbnails", exist_ok=True)
  
  for name, size in sizes.items():
    tn = image.copy()
    tn.thumbnail(size)
    tn_path = f"{tn_dir}/{name}.{file_extension}"
    tn.save(tn_path)
    thumbnails[name] = f"http://localhost:8000/api/images/{image_id}/thumbnails/{name}"
  
  return thumbnails

def generate_caption(image):
  # Use an AI to caption the image (using the BLIP model)
  inputs = processor(image, return_tensors="pt")
  out = model.generate(**inputs)
  return processor.decode(out[0], skip_special_tokens=True) 


# POST /api/images 
@app.post("/api/images")
async def upload_image(file: UploadFile = File(...)):
  try:
    start_time = time.time() # For time
    
    # Store file somewhere first
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
      f.write(file.file.read())

    load_image = Image.open(file.file)

    # Limit file upload to JPG and PNG
    if load_image.format.upper() not in ["JPEG", "PNG"]:
      os.remove(file_path)  # Clean up temporary file
      return JSONResponse(content={"status": "failure", "error": "Unsupported image file. Only accepts JPG or PNG files. Please try again."}, status_code=415)

    # Unique ID for image, using UUID
    image_id = str(uuid.uuid4())

    # Extract basic metadata (dimensions, format, size) 
    get_metadata = extract_metadata(load_image, file_path)

    # Generate thumbnails requirement (2 different sizes) 
    file_extension = "jpg" if load_image.format == "JPEG" else "png" # Since load.image returns JPEG
    get_thumbnails = generate_thumbnails(load_image, image_id, file_extension)

    # Use an AI to caption the image
    caption_text = generate_caption(load_image)

    # Response
    response = {
        "image_status": "success",
        "data": {
            "image_id": image_id,
            "original_name": file.filename,
            "processed_at": datetime.utcnow().isoformat() + "Z",
            "time_taken": round((time.time() - start_time), 2),
            "metadata": get_metadata,
            "thumbnails": get_thumbnails,
            "caption": caption_text
        },
        "error": None
    }
    # Store response in memory
    processed_results[image_id] = response

    # Update stats + flag
    processed_results_stats["success"] += 1
    processed_results_stats["total_processing_time"] += time.time() - start_time
    
    # Return
    os.remove(file_path)  # Clean up temporary file
    return JSONResponse(content=response, status_code=200)  

  except Exception as e:
    #raise HTTPException(status_code=400, detail="Something went wrong. Please try again.")
    # Update stats + flag
    processed_results_stats["failure"] += 1
    return JSONResponse(content={"status": "failure", "error": "Something went wrong. Please try again."}, status_code=400)
    #return JSONResponse(content={"status": "failure", "error": str(e)}, status_code=400)


# GET /api/images
# TODO: - Include processing status 
@app.get("/api/images")
async def list_images():
  try: 
    # Check if there is something inside first else return
    if not processed_results:
      return JSONResponse(content={"current_status": "success", "data": "No image has been processed yet.", "error": None}, status_code=200)
    return JSONResponse(content={"current_status": "success", "content": processed_results}, status_code=200)
  
  except Exception:
    return JSONResponse(content={"current_status": "failure", "error": "Something went wrong. Please try again."}, status_code=400)

# GET /api/images/{id} 
@app.get("/api/images/{image_id}")
async def get_image(image_id):
  try:
    # Check if image exists, then return true
    if image_id in processed_results:
      return JSONResponse(content={"current_status": "success", "data": processed_results[image_id]}, status_code=200)
    
    # Return image does not exist
    return JSONResponse(content={"current_status": "failure", "data": "Image does not exist. Please view another one.", "error": None}, status_code=404)
  
  except Exception:
      return JSONResponse(content={"current_status": "failure", "error": "Something went wrong. Please try again."}, status_code=400)

# GET /api/images/{id}/thumbnails/{small,medium} 
@app.get("/api/images/{image_id}/thumbnails/{size}")
async def get_thumbnails(image_id, size):
  try:
    # Check input for size
    if size not in ["small", "medium"]:
      return JSONResponse(content={"current_status": "failure", "error": "Invalid input size. Please use 'small' or 'medium'."}, status_code=400)

    # Check for file path, then return True
    extensions = ["jpg", "png"]
    tm_dir = f"{image_id}/thumbnails"
    for ext in extensions:
      tn_path = f"{tm_dir}/{size}.{ext}"
      if os.path.exists(tn_path):
        return JSONResponse(content={"current_status": "success", "data": tn_path}, status_code=200)
    
    # Return false if not found
    return JSONResponse(content={"current_status": "failure", "error": "Thumbnail not found."}, status_code=404)
  except Exception:
    return JSONResponse(content={"current_status": "failure", "error": "Something went wrong. Please try again."}, status_code=400)


# GET /api/stats 
# TODO: - Processing statistics
@app.get("/api/stats")
async def get_stats():
  try:
    # Get total time taken / number of items = average time taken
    if processed_results_stats["success"] > 0:
      processed_results_stats["avg_processing_time"] = (
        processed_results_stats["total_processing_time"] / processed_results_stats["success"]
      )
    else:
      processed_results_stats["avg_processing_time"] = 0

    return JSONResponse(content={"current_status": "success", "data": processed_results_stats}, status_code=200)
  
  except Exception:
    return JSONResponse(content={"current_status": "failure", "error": "Something went wrong. Please try again."}, status_code=400)
  
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)