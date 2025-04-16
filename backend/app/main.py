from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
