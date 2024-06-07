from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,File
from fastapi.responses import JSONResponse ,FileResponse
from helpers.config import get_settings ,Settings
from models.enums.ResponseEnum import ResponseSignal
from controllers import ConverterController
import os
import tempfile
from PIL import Image
import io


converter_router = APIRouter(
    prefix="/api/v1/converter",
    tags=["api_v1" , "converter"],
)





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
        temp_pdf_path = f"/tmp/{file.filename}"
        with open(temp_pdf_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        extracted_text = ConverterController().extract_text_from_pdf(temp_pdf_path)
        if not extracted_text:
                    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                     content={
                                             "signal" : ResponseSignal.PROCESSING_FAILED.value
                                     })

        temp_txt_path = f"/tmp/{file.filename}.txt"
        with open(temp_txt_path, "w") as temp_file:
            temp_file.write(extracted_text)

        return FileResponse(temp_txt_path, filename=f"{file.filename}.txt" , status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROCESSING_FAILED.value , "error":str(e)}
        )

