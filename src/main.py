from fastapi import FastAPI
from routes import base , converter ,compressor

app = FastAPI()

app.include_router(base.base_router)
app.include_router(converter.converter_router)
app.include_router(compressor.compressor_router)
