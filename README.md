# Lab Report Extraction API

This FastAPI service extracts lab test names, values, units, and reference ranges from uploaded lab report images.

## Features

- Accepts lab report images via POST request
- Uses OCR (pytesseract) to extract text
- Parses lab test name, value, unit, and reference range
- Flags if the test value is out of the reference range
- Returns structured JSON output

## Sample
![image](https://github.com/user-attachments/assets/6a276610-3eda-4e4b-9cb9-f02c0fcb9b84)

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
