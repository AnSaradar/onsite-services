from fastapi import FastAPI
from routes import base , converter

app = FastAPI()

app.include_router(base.base_router)
app.include_router(converter.converter_router)

