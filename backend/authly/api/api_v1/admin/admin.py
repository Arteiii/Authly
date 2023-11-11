"""
main.py
"""
from fastapi import APIRouter

from authly.api.api_v1.authentication import user_authorization as ua

app = APIRouter()

@app.post("/")
async def create_admin():


@app.get("/")

@app.get("/user") # get user data

@app.get("/log") # get latest logs