from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import io
import re
from pypdf import PdfReader
from PIL import Image
import pytesseract

app = FastAPI()

class LabTest(BaseModel):
    test_name: str
    test_value: float
    bio_reference_range: str
    test_unit: str
    lab_test_out_of_range: bool

class LabTestResponse(BaseModel):
    is_success: bool
    data: List[LabTest]

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

@app.post("/get-lab-tests", response_model=LabTestResponse)
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        filename = file.filename.lower()
        text = ""
        if filename.endswith('.pdf'):
            pdf_bytes = await file.read()
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            if not text.strip():
                return JSONResponse(
                    status_code=400,
                    content={"is_success": False, "data": [], "error": "No extractable text found in PDF. If your PDF is scanned, please upload as an image."}
                )
        else:
            image_bytes = await file.read()
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
        lab_tests = parse_lab_tests(text)
        return LabTestResponse(is_success=True, data=lab_tests)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"is_success": False, "data": [], "error": str(e)}
        )
