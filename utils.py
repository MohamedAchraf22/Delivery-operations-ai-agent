from typing import Any, Dict, List, Optional


def get_nested(d: Any, *keys: str) -> Any:
    for key in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(key)
    return d


def summarize(orders: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for o in orders:
        rows.append({
            "id": o.get("id"),
            "tracking_number": o.get("tracking_number"),
            "status": o.get("status"),
            "created": o.get("created"),
            "pickup_date": o.get("pickup_date"),
            "delivered_date": o.get("delivered_date"),
            "cash_amount": o.get("cash_amount"),
            "delivery_attempts": o.get("delivery_attempts"),
            "is_exchange": o.get("is_exchange"),
            "city": get_nested(o, "customer", "address", "zone", "city", "name"),
            "governorate": get_nested(o, "customer", "address", "zone", "city", "governorate", "name"),
        })
    return rows


def flatten_order(o: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": o.get("id"),
        "tracking_number": o.get("tracking_number"),
        "status": o.get("status"),
        "created": o.get("created"),
        "pickup_date": o.get("pickup_date"),
        "delivered_date": o.get("delivered_date"),
        "cash_amount": o.get("cash_amount"),
        "delivery_attempts": o.get("delivery_attempts"),
        "is_exchange": o.get("is_exchange"),
        "merchant_order_reference": o.get("merchant_order_reference"),
        "customer_name": get_nested(o, "customer", "full_name"),
        "customer_phone": get_nested(o, "customer", "phone"),
        "address": get_nested(o, "customer", "address", "line_1"),
        "city": get_nested(o, "customer", "address", "zone", "city", "name"),
        "governorate": get_nested(o, "customer", "address", "zone", "city", "governorate", "name"),
    }

