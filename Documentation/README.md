# API Documentation
This documentation here provides a detailed information about the available API endpoints, and their usage:

### Base URL
All API endpoinits are relative to the base URL: `http://127.0.0.1:8000`

#### 1. Uploading an Image
Uploads an image for processing. The workflow can be seen from [here](#process-flow). The API will generate thumbnails, extract metadata, and generate a caption.
- **URL**: `/api/images`
- **Method**: `POST`
- **Request Body**:
  - **Content-Type**: `multipart/form-data`
  - **Parameters**: key -> `file`, value -> the image file to upload
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - <details><summary>Example Response</summary><p>
  ```json
  {
    "image_status": "success",
    "data": {
        "image_id": "15ea78c8-24eb-4ea4-92a2-87b1f0aa7b87",
        "original_name": "dark.jpg",
        "processed_at": "2025-03-16T03:58:35.311830Z",
        "time_taken": 5.69,
        "metadata": {
            "width": 626,
            "height": 417,
            "format": "JPEG",
            "size_bytes": 25932,
            "created_at": "2025-03-16 11:58:29",
            "modified_at": "2025-03-16 11:58:29"
        },
        "thumbnails": {
            "small": "http://localhost:8000/api/images/15ea78c8-24eb-4ea4-92a2-87b1f0aa7b87/thumbnails/small",
            "medium": "http://localhost:8000/api/images/15ea78c8-24eb-4ea4-92a2-87b1f0aa7b87/thumbnails/medium"
        },
        "caption": "a dark background with a yellow light"
    },
    "error": null
    }
  ```
  </p></details>
- **Error Response**:
  - **Code**: `415 Unsupported Media Type`
  - **Returned Content**: JSON Response
  - <details><summary>Example Response</summary><p>
  ```json
  {
    "current_status": "failure",
    "error": "Unsupported image file. Only accepts JPG or PNG files. Please try again."
    }
  ```
    </p></details>
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

#### 2. List All Processed Images
Retrieve a list of all processed images.
- **URL**: `/api/images`
- **Method**: `GET`
- **Success Response - No images processed yet**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
- **Success Response - There are processed images in memory**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - <details><summary>Example Response</summary><p>
  ```json
  {
    "current_status": "success",
    "data": "No image has been processed yet.",
    "error": null
    }
  ```
  </p></details>
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response
  - <details><summary>Example Response</summary><p>
  ```json
    {
    "detail": "There was an error parsing the body"
    }
  ```
    </p></details>

#### 3. Get An Image Details
Retrieve details of a specific image, including metadata, thumbnails, and caption.
- **URL**: `/api/images/{image_id}`
- **Method**: `GET`
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
- **Error Response - Specified image does not exist**:
  - **Code**: `404 Not Found`
  - **Returned Content**: JSON Response
- **Error Response - Something Happened**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

#### 4. Get Thumbnail
Retrieve a specific image thumbnail (small/medium).
- **URL**: `/api/images/{image_id}/thumbnails{small,medium}`
- **Method**: `GET`
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
- **Error Response - User input for size not small or medium**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response
- **Error Response - Thumbnail not found**:
  - **Code**: `404 Not Found`
  - **Returned Content**: JSON Response
- **Error Response - Something Happened**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

#### 5. Get Processing Statistics
Retrieve the statistics about the processed image(s), including the number of success and failure, and average processing time.
- **URL**: `/api/stats`
- **Method**: `GET`
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

#### Error Handling
All error handling follows the same format:
```json
{
  "current_status": "failure",
  "error": "Error message"
}
```