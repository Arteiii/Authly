"""
main.py
"""
from api.api_router import api_main_router
from core.config import config
from fastapi import FastAPI

app = FastAPI()


app.include_router(api_main_router, prefix=config.API.API_ROUTE)


# debug/dev only
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
