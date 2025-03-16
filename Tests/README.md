# Test Cases
In this section, the test cases primarily focuses on the following API:
1. Uploading an image -> POST /api/images
2. Retriving processed statsitics -> GET /api/stats
3. Generation of captions that uses an AI to caption the image (using the BLIP model)

The test cases are to simulate the API calls using FastAPI's fake client (TestClient(app)), allowing requests without running a server. Essentially it is to mock actual requests like POST and GET to get responses like a real API call

## Pre-requisites
1. Install the necessary dependencies:
```
pip install -r requirements.txt
```

## Running the Test Cases
In CMD, run the following command:
```
pytest test_main.py
```
The test cases should pass as shown in the example output below:
```
#pytest test_main.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-8.3.5, pluggy-1.5.0
rootdir: D:\github_projects\image_processing_api\Tests
plugins: anyio-4.8.0
collected 3 items

test_main.py ...                                                                                                 [100%]

================================================== warnings summary ===================================================
test_main.py::test_upload_image
test_main.py::test_generate_caption
  D:\github_projects\image_processing_api\main.py:100: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "processed_at": datetime.utcnow().isoformat() + "Z",

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 3 passed, 2 warnings in 10.49s ============================================
```

## References:
- Assert usage [ttps://realpython.com/python-assert-statement/]
- [AI](https://chatgpt.com/) used to resolve error of adding absolute path to import FastAPI (app) 