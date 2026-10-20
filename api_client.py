from typing import Any, Dict, List, Optional
import requests
from config import BASE_URL, HEADERS
from utils import get_nested


def get_order_by_id(order_id: int) -> Dict[str, Any]:
    resp = requests.get(
        f"{BASE_URL}/delivery-orders/{order_id}/",
        headers=HEADERS,
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()


def fetch_orders(
    status: Optional[str] = None,
    status_except: Optional[str] = None,
    tracking_number: Optional[str] = None,
    phone: Optional[str] = None,
    merchant_order_reference: Optional[str] = None,
    is_exchange: Optional[bool] = None,
    delivery_attempts: Optional[str] = None,
    cash_amount__gt: Optional[float] = None,
    cash_amount: Optional[float] = None,
    created: Optional[str] = None,
    pickup_date: Optional[str] = None,
    delivered_date: Optional[str] = None,
    city: Optional[str] = None,
    governorate: Optional[str] = None,
) -> List[Dict[str, Any]]:
    params = {
        "status": status,
        "status_except": status_except,
        "tracking_number": tracking_number,
        "phone": phone,
        "merchant_order_reference": merchant_order_reference,
        "is_exchange": None if is_exchange is None else str(is_exchange).lower(),
        "delivery_attempts": delivery_attempts,
        "cash_amount": cash_amount,
        "cash_amount__gt": cash_amount__gt,
        "created": created,
        "pickup_date": pickup_date,
        "delivered_date": delivered_date,
        "limit": 100,
    }
    url = f"{BASE_URL}/delivery-orders/"
    all_results = []

    while url:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        all_results.extend(data.get("results", []))
        url = data.get("next")

    if city:
        all_results = [
            o for o in all_results
            if (get_nested(o, "customer", "address", "zone", "city", "name") or "").lower() == city.lower()
        ]
    if governorate:
        all_results = [
            o for o in all_results
            if (get_nested(o, "customer", "address", "zone", "city", "governorate", "name") or "").lower() == governorate.lower()
        ]

    return all_results

