from .BaseController import BaseController
from models.enums.ResponseEnum import ResponseSignal
from fastapi import UploadFile
import PyPDF2

class ConverterController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576 # convert MB to bytes


    def validate_pdf_uploaded_file(self, file : UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.FILE_MAX_SIZE_EXCEEDED.value

        return True,ResponseSignal.FILE_VALIDATE_SUCCESS.value
    

    def extract_text_from_pdf(self , pdf_path):
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