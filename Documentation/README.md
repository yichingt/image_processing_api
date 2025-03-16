# Table of Content
- [Processing Pipeline Documentation](#processing-pipeline-documentation)
- [API Documentation](#api-documentation)

# Processing Pipeline Documentation
This section describes the workflow of the Image Processing Pipeline API, from uploading the image to the final response generated.
<img src="./upload_file_process_workflow.png" alt="uploading image success" width="600"/>

## 1. Uploading an Image
- User uploads an image file (JPG or PNG) via the POST /api/images
- The API will receive the file and first validate its format.
### 1.1 Validation
- The API will check if the uploaded file is in a valid file format (i.e. JPG or PNG)
- If the file is valid, it will continue forward. If the file is invalid, it will return 415 status code for `Unsupported Media Type`.

## 2. Processing, Genrating ID and Retriving Metadata
</b>If the image is valid, the API will process the following steps:

1. Generate a Unique ID using UUID: A unique ID will be generated for the image

2. Extract required metadata:
- The API will extract the followiing metadata from the image:
  - Dimensions
  - File Format
  - File Size
  - Creation Date
  - Modified Date
  
3. Generate thumbnails:
- The API will generate 2 thumbnails for the image:
  - Small (128,128)
  - Medium (512, 512)
- The thumbnails will then be saved locally, and their URLs are included in the JSON response

4. Generate Captions:
The API will use a pre-trained AI model (Blip Image Captioning) to generate a caption for the image

5. Storing the Results:
The output results will be stored in the memory, where each results are associated with the unique ID.

6. Return Response:
The API will return a JSON response containing the following:
- Unique Image ID
- File's Original Name
- Processing time taken
- Extracted metadata
- Thumbnails' URLs
- AI-generated caption

# API Documentation
This section here provides a detailed information about the available API endpoints, and their usage:
- [Base URL](#base-url)
- [Uploading an Image](#1-uploading-an-image)
- [List All Processed Images](#2-list-all-processed-images)
- [Get An Image Details](#3-get-an-image-details)
- [Get Thumbnail](#4-get-thumbnail)
- [Get Processing Statisitcs](#5-get-processing-statistics)
- [Error Handling](#error-handling)

### Base URL
All API endpoinits are relative to the base URL: `http://127.0.0.1:8000`

### 1. Uploading an Image
Uploads an image for processing. The workflow can be seen from [here](#process-flow). The API will generate thumbnails, extract metadata, and generate a caption. The caption actually uses AI (Blip Image Captioning) to generate them.
- **URL**: `/api/images`
- **Method**: `POST`
- **Request Body**:
  - **Content-Type**: `multipart/form-data`
  - **Parameters**: key -> `file`, value -> the image file to upload
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "image_status": "success",
    "data": {
        "image_id": "b480bcff-7fff-45b2-93cf-7a534fe39821",
        "original_name": "hehhhh.jpg",
        "processed_at": "2025-03-16T07:09:30.826114+00:00",
        "time_taken": 3.21,
        "metadata": {
            "width": 261,
            "height": 216,
            "format": "JPEG",
            "size_bytes": 13962,
            "created_at": "2025-03-16 15:09:27",
            "modified_at": "2025-03-16 15:09:27"
        },
        "thumbnails": {
            "small": "http://localhost:8000/api/images/b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/small",
            "medium": "http://localhost:8000/api/images/b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/medium"
        },
        "caption": "a cartoon picture of two people standing in front of a city"
    },
    "error": null
  }
    ```
- **Error Response**:
  - **Code**: `415 Unsupported Media Type`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "failure",
    "error": "Unsupported image file. Only accepts JPG or PNG files. Please try again."
    }
  ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

### 2. List All Processed Images
Retrieve a list of all processed images.
- **URL**: `/api/images`
- **Method**: `GET`
- **Success Response - There are processed images in memory**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "success",
    "content": {
        "b480bcff-7fff-45b2-93cf-7a534fe39821": {
            "image_status": "success",
            "data": {
                "image_id": "b480bcff-7fff-45b2-93cf-7a534fe39821",
                "original_name": "hehhhh.jpg",
                "processed_at": "2025-03-16T07:09:30.826114+00:00",
                "time_taken": 3.21,
                "metadata": {
                    "width": 261,
                    "height": 216,
                    "format": "JPEG",
                    "size_bytes": 13962,
                    "created_at": "2025-03-16 15:09:27",
                    "modified_at": "2025-03-16 15:09:27"
                },
                "thumbnails": {
                    "small": "http://localhost:8000/api/images/b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/small",
                    "medium": "http://localhost:8000/api/images/b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/medium"
                },
                "caption": "a cartoon picture of two people standing in front of a city"
            },
            "error": null
        },
        "f9fb3888-66f6-4dfb-a7dd-63b286f19292": {
            "image_status": "success",
            "data": {
                "image_id": "f9fb3888-66f6-4dfb-a7dd-63b286f19292",
                "original_name": "holdhands.JPG",
                "processed_at": "2025-03-16T07:11:14.231146+00:00",
                "time_taken": 1.45,
                "metadata": {
                    "width": 505,
                    "height": 488,
                    "format": "JPEG",
                    "size_bytes": 60953,
                    "created_at": "2025-03-16 15:11:12",
                    "modified_at": "2025-03-16 15:11:12"
                },
                "thumbnails": {
                    "small": "http://localhost:8000/api/images/f9fb3888-66f6-4dfb-a7dd-63b286f19292/thumbnails/small",
                    "medium": "http://localhost:8000/api/images/f9fb3888-66f6-4dfb-a7dd-63b286f19292/thumbnails/medium"
                },
                "caption": "two hands reaching each other hand"
            },
            "error": null
        }
    }
  }
  ```
- **Success Response - No images processed yet**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "success",
    "data": "No image has been processed yet.",
    "error": null
    }
  ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
    {
    "detail": "There was an error parsing the body"
    }
  ```

### 3. Get An Image Details
Retrieve details of a specific image, including metadata, thumbnails, and caption.
- **URL**: `/api/images/{image_id}`
- **Method**: `GET`
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "success",
    "data": {
        "image_status": "success",
        "data": {
            "image_id": "b480bcff-7fff-45b2-93cf-7a534fe39821",
            "original_name": "hehhhh.jpg",
            "processed_at": "2025-03-16T07:09:30.826114+00:00",
            "time_taken": 3.21,
            "metadata": {
                "width": 261,
                "height": 216,
                "format": "JPEG",
                "size_bytes": 13962,
                "created_at": "2025-03-16 15:09:27",
                "modified_at": "2025-03-16 15:09:27"
            },
            "thumbnails": {
                "small": "http://localhost:8000/api/images/b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/small",
                "medium": "http://localhost:8000/api/images/b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/medium"
            },
            "caption": "a cartoon picture of two people standing in front of a city"
        },
        "error": null
    }
  }
    ```
- **Error Response - Specified image does not exist**:
  - **Code**: `404 Not Found`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "failure",
    "data": "Image does not exist. Please view another one.",
    "error": null
    }
  ```
- **Error Response - Something Happened**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

### 4. Get Thumbnail
Retrieve a specific image thumbnail (small/medium).
- **URL**: `/api/images/{image_id}/thumbnails{small,medium}`
- **Method**: `GET`
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "success",
    "data": "b480bcff-7fff-45b2-93cf-7a534fe39821/thumbnails/small.jpg"
  }
  ```
- **Error Response - User input for size not small or medium**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response
  - **Example Content**:
  ```json
  {
    "current_status": "failure",
    "error": "Invalid input size. Please use 'small' or 'medium'."
    }
  ```
- **Error Response - Thumbnail not found**:
  - **Code**: `404 Not Found`
  - **Returned Content**: JSON Response
  - **Example Content**:
  ```json
  {
    "current_status": "failure",
    "error": "Thumbnail not found."
    }
  ```
- **Error Response - Something Happened**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

### 5. Get Processing Statistics
Retrieve the statistics about the processed image(s), including the number of success and failure, and average processing time.
- **URL**: `/api/stats`
- **Method**: `GET`
- **Success Response**:
  - **Code**: `200 OK`
  - **Returned Content**: JSON Response
  - **Example Response**:
  ```json
  {
    "current_status": "success",
    "data": {
        "success": 2,
        "failure": 0,
        "total_processing_time": 4.662299156188965,
        "avg_processing_time": 2.3311495780944824
    }
  }
  ```
- **Error Response**:
  - **Code**: `400 Bad Request`
  - **Returned Content**: JSON Response

### Error Handling
All error handling follows the same format:
```json
{
  "current_status": "failure",
  "error": "Error message"
}
```