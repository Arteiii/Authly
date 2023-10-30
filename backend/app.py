from api.api_router import api_main_router
from core.config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

Debug = False

origins = [
    "*"
]  # list of origins which are allowed to make requests to the api
# (default: "*")

app = FastAPI()


if Debug is True:
    print("Security Middleware Disabled for debugging")
else:
    print("Security Middleware Active!!")
    # Handles Cross-Origin Resource Sharing (CORS) settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Enables GZIP compression for responses,
    # reducing the size of transmitted data.
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Redirects HTTP requests to HTTPS for secure communication
    app.add_middleware(HTTPSRedirectMiddleware)
    # NOTE: add config checks for it later

    # Ensures that the application only accepts requests from trusted hosts.
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=["*"]
    )  # Replace "*" with your trusted hosts


# Include the API router
app.include_router(api_main_router, prefix=config.API.API_ROUTE)

# Debug/development mode only
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="localhost", port=8000)
