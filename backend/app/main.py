from fastapi import FastAPI

app = FastAPI()

# Import routers (next step will link these routes)
from routes import brain_tumor, general_image

app.include_router(brain_tumor.router, prefix="/api/brain-tumor")
app.include_router(general_image.router, prefix="/api/general-analysis")
