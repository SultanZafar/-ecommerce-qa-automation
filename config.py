import os

# Override these with environment variables if your app runs elsewhere, e.g.:
#   WEB_BASE_URL=http://localhost:5500 API_BASE_URL=http://localhost:4000/api pytest
WEB_BASE_URL = os.environ.get("WEB_BASE_URL", "http://localhost:5500")
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:4000/api")

DEFAULT_TIMEOUT_MS = 8000
