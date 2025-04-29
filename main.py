# Headers to import
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from PIL import Image
import pytesseract
import io
import re

# Initialising FastAPI
app = FastAPI()

# To run:
# uvicorn app:app --reload

# Defining class for Lab Test
class LabTest(BaseModel):
    test_name: str
    test_value: float
    bio_reference_range: str
    test_unit: str
    lab_test_out_of_range: bool

# Defining class for Lab Test Response(Success/Failure)
class LabTestResponse(BaseModel):
    is_success: bool
    data: List[LabTest]

# Extracting data from image using Pytesseract
def parse_lab_tests(text: str) -> List[LabTest]:
    pattern = re.compile(
        r"([A-Za-z\s\(\)]+)\s+([\d.]+)\s*([^\d\s]+)?\s+\(?([\d.]+)\s*-\s*([\d.]+)\)?"
    )

    results = []
    for match in pattern.finditer(text):
        test_name = match.group(1).strip()
        test_value = float(match.group(2))
        unit = match.group(3) if match.group(3) else ""
        ref_low = float(match.group(4))
        ref_high = float(match.group(5))
        out_of_range = not (ref_low <= test_value <= ref_high)
        results.append(LabTest(
            test_name=test_name,
            test_value=test_value,
            bio_reference_range=f"{ref_low}-{ref_high}",
            test_unit=unit,
            lab_test_out_of_range=out_of_range
        ))
    return results


# API Endpoint  
@app.post("/get-lab-tests", response_model=LabTestResponse)
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        # Image to PIL Image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        # Image to String  
        text = pytesseract.image_to_string(image)
        lab_tests = parse_lab_tests(text)
        return LabTestResponse(is_success=True, data=lab_tests)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"is_success": False, "data": [], "error": str(e)}
        )
