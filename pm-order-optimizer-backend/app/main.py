from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(find_dotenv(), override=True)

from fastapi import FastAPI
from .routers import orders
import os

fronted_url = os.getenv("FRONTEND_DEV_URL")

origins = []
if fronted_url:
    origins.append(fronted_url)
print("origins: " + str(origins))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router, prefix="/orders", tags=["orders"])
