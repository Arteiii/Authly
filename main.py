import uvicorn
import hypercorn
import sys
from authly import app


def run_development():
    # Development configuration
    # Start the FastAPI application using uvicorn
    # 'authly.app:app': The import string representing the location of the FastAPI instance
    #                Replace 'authly' with the actual name of your package, and 'app' with the FastAPI instance
    # host="127.0.0.1": The IP address to bind the server to. In this case, it's localhost
    # port=8000: The port number on which the server will listen for incoming connections
    # reload=True: Enables automatic code reloading when changes are detected during development
    uvicorn.run(
        "authly.app:app", host="127.0.0.1", port=8000, log_level="debug", reload=True
    )

    # log_level="debug": The log level for uvicorn. Controls the verbosity of log messages
    #   critical: Only very serious errors that may lead the application to crash
    #   error: General errors that do not necessarily lead to a crash but indicate a problem
    #   warning: Warnings about potential issues or unexpected behavior
    #   info (default): General information about the application's operation
    #   debug: Detailed information for debugging purposes. More verbose than info
    #   trace: Extremely detailed information, including low-level details. Most verbose


def run_production():
    # Production configuration using Hypercorn
    config = hypercorn.Config.from_mapping(
        bind="0.0.0.0:8000",  # Specify the host and port
        loglevel="error",  # Log level (error for production)
        workers=2,  # Number of worker processes (adjust as needed)
        # Additional Hypercorn configuration options can be added here
    )

    hypercorn.run(app.app, config=config)


def run_custom(**kwargs):
    # Custom configuration using provided keyword arguments
    uvicorn.run("authly.app:app", **kwargs)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ["development", "production", "custom"]:
        print("Usage:")
        print("Development: python main.py development")
        print("Production: python main.py production")
        print(
            "Custom: python main.py custom --host=127.0.0.1 --port=8000 --log-level=debug --reload"
        )
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "development":
        run_development()
    elif mode == "production":
        run_production()
    elif mode == "custom":
        # Extract command-line arguments for custom mode (skipping the script name and mode)
        custom_args = sys.argv[2:]
        # Convert arguments to a dictionary
        custom_kwargs = dict(arg.split("=") for arg in custom_args)
        run_custom(**custom_kwargs)


if __name__ == "__main__":
    main()
