"""
main.py
"""
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/admin/token")

app = APIRouter()
