from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(find_dotenv(), override=True)

from fastapi import FastAPI
from .routers import orders

origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, prefix="/orders", tags=["orders"])
