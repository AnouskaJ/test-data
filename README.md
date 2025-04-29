# Lab Report Extraction API

This FastAPI service extracts lab test names, values, units, and reference ranges from uploaded lab report images.

## Deployed Edpoint
https://test-data-e7ez.onrender.com/get-lab-tests

## Features

- Accepts lab report images via POST request
- Uses OCR (pytesseract) to extract text
- Parses lab test name, value, unit, and reference range
- Flags if the test value is out of the reference range
- Returns structured JSON output

## Sample
![Screenshot 2025-04-29 114138](https://github.com/user-attachments/assets/0c481c63-3f8c-4a74-9e93-5e3617c1ae7c)

## How to Run

1. **Install dependencies:**
    ```
    pip install fastapi uvicorn pillow pytesseract
    ```

2. **Start the server:**
    ```
    uvicorn app:app --reload
    ```

3. **Use the API:**
    - Endpoint: `POST /get-lab-tests`
    - Form field: `file` (image file)

## Output Example

```json
{
  "is_success": true,
  "data": [
    {
      "test_name": "HB ESTIMATION",
      "test_value": 9.4,
      "bio_reference_range": "12.0-15.0",
      "test_unit": "g/dl",
      "lab_test_out_of_range": true
    }
  ]
}
```
