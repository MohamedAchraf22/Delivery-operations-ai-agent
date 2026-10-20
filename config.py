import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("SHIPBLU_BASE_URL", "http://localhost:8000/api/v1")
API_KEY = os.environ.get("SHIPBLU_API_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

HEADERS = {
    "Authorization": f"Api-Key {API_KEY}"
}

DEFAULT_COLUMNS = [
    "tracking_number",
    "status",
    "created",
    "delivered_date",
    "cash_amount",
    "customer_name",
    "customer_phone",
    "city",
    "governorate"
]

EXPORTS_DIR = Path("exports")

