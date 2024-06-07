from .BaseController import BaseController
from models.enums.ResponseEnum import ResponseSignal
from fastapi import UploadFile
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,File , Form, HTTPException
from PIL import Image
import mimetypes
import os

class CompressorController(BaseController):

    def __init__(self):
        super().__init__()

    def is_image_file(self , file: UploadFile):
   
        mimetypes.init()
        mime_type, _ = mimetypes.guess_type(file.filename)
        valid_mime_types = ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/webp"]
        valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
        file_extension = os.path.splitext(file.filename)[1].lower()
        is_image =  mime_type in valid_mime_types and file_extension in valid_extensions
        
        if not is_image:
            return False , ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        else:
            return True , ResponseSignal.FILE_VALIDATE_SUCCESS.value

    
    def compress_image(self ,image: Image.Image, compress_percentage: float) -> Image.Image:
        
        width, height = image.size
        new_width = int(width * (compress_percentage / 100))
        new_height = int(height * (compress_percentage / 100))
        img = image.resize((new_width, new_height), Image.LANCZOS)
        return img


    