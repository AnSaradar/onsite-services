from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,File
from fastapi.responses import JSONResponse
from helpers.config import get_settings ,Settings
from models.enums.ResponseEnum import ResponseSignal
from controllers import ConverterController
from fastapi.responses import FileResponse
import os
import PyPDF2
import tempfile
from PIL import Image
import io


converter_router = APIRouter(
    prefix="/api/v1/converter",
    tags=["api_v1" , "converter"],
)

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"  # Adding newline for better readability
                
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None



@converter_router.post("/pdf_to_text")
async def pdf_to_text(file : UploadFile = File(...)):

    temp_file_path = ""
    text_file_path = ""

    is_valid , result_signal = ConverterController().validate_pdf_uploaded_file(file)

    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                     content={
                                             "signal" : result_signal
                                     })
    # else:
    #     return JSONResponse(status_code=status.HTTP_200_OK,content={"message":result_signal})
     
    try:
        # Save the uploaded PDF file temporarily
        temp_pdf_path = f"/tmp/{file.filename}"
        with open(temp_pdf_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(temp_pdf_path)
        if not extracted_text:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                     content={
                                             "signal" : ResponseSignal.PROCESSING_FAILED.value
                                     })

        # Save the extracted text to a temporary text file
        temp_txt_path = f"/tmp/{file.filename}.txt"
        with open(temp_txt_path, "w") as temp_file:
            temp_file.write(extracted_text)

        # Return the text file as a response
        return FileResponse(temp_txt_path, filename=f"{file.filename}.txt" , status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROCESSING_FAILED.value , "error":str(e)}
        )

@converter_router.post("/image-compress/{compress_percentage}")
async def compress_image(compress_percentage : int,file: UploadFile = File(...)):
    try:
            # Read image file
        image = Image.open(file.file)
        
        # Compress the image
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=compress_percentage)  # Quality from 0 to 100, 20 is fairly low quality
        
        buffer.seek(0)
        
        # Save or return the compressed image
        return FileResponse(buffer, media_type="image/jpeg", filename=f"compressed_{file.filename}",
                            status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROCESSING_FAILED.value , "error":str(e)}
        )
