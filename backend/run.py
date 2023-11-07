import os
import sys
import uvicorn

# Set the root directory to outside the backend module
root_directory = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../")
)
print(f"root: {root_directory}")
sys.path.insert(0, root_directory)


uvicorn.run("backend.authly.app:app", host="localhost", port=8000)
