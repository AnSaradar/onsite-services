from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,File , Form, HTTPException
from fastapi.responses import JSONResponse , StreamingResponse ,FileResponse
from helpers.config import get_settings ,Settings
from models.enums.ResponseEnum import ResponseSignal
from controllers import CompressorController
from PIL import Image
import io
import mimetypes
import os

compressor_router = APIRouter(
    prefix="/api/v1/compressor",
    tags=["api_v1" , "compressor"],
)




@compressor_router.post("/image-compress")
async def compress_image_endpoint(
    file: UploadFile = File(...), 
    compress_percentage: float = Form(...)
):
    
    is_image =  CompressorController().is_image_file(file)
    if not is_image :
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                     content={
                                             "signal" : "HTTP_400_BAD_REQUEST"
                                     })
    try:
        image = Image.open(file.file)
        
        compressed_image = CompressorController().compress_image(image, compress_percentage)
        
        buf = io.BytesIO()
        compressed_image.save(buf, format="JPEG", optimize=True, quality=85)
        buf.seek(0)
        
        return StreamingResponse(buf, media_type="image/jpeg",status_code=status.HTTP_200_OK)
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": ResponseSignal.PROCESSING_FAILED.value , "error":str(e)}
        )