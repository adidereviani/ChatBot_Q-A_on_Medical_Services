from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include the API router
app.include_router(router)
