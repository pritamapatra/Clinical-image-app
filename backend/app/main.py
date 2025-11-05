from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import routers (next step will link these routes)
from app.routes import brain_tumor, general_image,brain_hemorrhage

app.include_router(brain_tumor.router, prefix="/api/brain-tumor")
app.include_router(general_image.router, prefix="/api/general-analysis")
app.include_router(brain_hemorrhage.router, prefix="/brain-hemorrhage")

