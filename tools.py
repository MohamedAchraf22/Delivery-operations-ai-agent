from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional
import pandas as pd
import requests
from langchain_classic.agents import tool
from config import DEFAULT_COLUMNS, EXPORTS_DIR
from utils import flatten_order, summarize
from api_client import fetch_orders, get_order_by_id


@tool
def get_order(order_id: int):
    """-this tool is used when need to know about specific order using order id
    -If you only have a tracking number, call list_orders(tracking_number=...) first to get the id.
    """
    try:
        return get_order_by_id(order_id)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"order : {order_id} doesn't exists"
        return f"there's an error {e.response.status_code} in the request"


@tool
def list_orders(
    status: Optional[str] = None,
    status_except: Optional[str] = None,
    tracking_number: Optional[str] = None,
    phone: Optional[str] = None,
    merchant_order_reference: Optional[str] = None,
    is_exchange: Optional[bool] = None,
    delivery_attempts: Optional[str] = None,
    cash_amount__gt: Optional[float] = None,
    created: Optional[str] = None,
    pickup_date: Optional[str] = None,
    delivered_date: Optional[str] = None,
    city: Optional[str] = None,
    governorate: Optional[str] = None,
    cash_amount: Optional[float] = None,
):
    """Fetch delivery orders (all pages) with optional filters.
    status: exact status, e.g. 'delivered', 'returned', 'in_transit'.
    status_except: all orders EXCEPT this status.
    tracking_number: e.g. 'SB668544062'.
    phone: customer phone number.
    merchant_order_reference: merchant's own reference, e.g. 'REF-3481'.
    is_exchange: True for exchange orders only, False to exclude them.
    delivery_attempts: one of '0', '1', '2', '3', 'more_than_3'.
    cash_amount: orders with COD amount EXACTLY equal to this value.
    cash_amount__gt: orders with COD amount strictly greater than this value.
    Do not use cash_amount__gt to mean "equal to".
    created: date the order was created, format YYYY-MM-DD (single day) not a range for several days, call the tool once per day.
    pickup_date: date the courier picked it up, format YYYY-MM-DD (single day) not a range for several days, call the tool once per day.
    delivered_date: date it was delivered, format YYYY-MM-DD (single day) not a range for several days, call the tool once per day.
    city: city name in English, e.g. 'New Cairo', 'Sheikh Zayed'.
    governorate: governorate name in English, e.g. 'Giza', 'Cairo', 'Alexandria'.
    """
    try:
        orders = fetch_orders(
            status=status,
            status_except=status_except,
            tracking_number=tracking_number,
            phone=phone,
            merchant_order_reference=merchant_order_reference,
            is_exchange=is_exchange,
            delivery_attempts=delivery_attempts,
            cash_amount__gt=cash_amount__gt,
            cash_amount=cash_amount,
            created=created,
            pickup_date=pickup_date,
            delivered_date=delivered_date,
            city=city,
            governorate=governorate,
        )
        final_result = summarize(orders)

        if len(final_result) <= 50:
            return {"total_count": len(final_result), "orders": final_result}
        return {
            "total_count": len(final_result),
            "total_cash": sum(r["cash_amount"] or 0 for r in final_result),
            "by_status": dict(Counter(r["status"] for r in final_result)),
            "by_city": dict(Counter(r["city"] for r in final_result)),
            "sample": final_result[:20],
            "note": "Only 20 of the orders are shown. For the full list, export to Excel.",
        }
    except requests.exceptions.HTTPError as e:
        return f"error {e.response.status_code}"


@tool
def export_orders_to_excel(
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
    columns: Optional[List[str]] = None,
):
    """Export ALL matching delivery orders to an Excel file and return the file path.
    Use this when the user asks for a sheet / Excel / spreadsheet / file.
    Filters work exactly like list_orders (same names and formats).

    columns: optional list of columns to include. If the user does not ask for
    specific columns, leave it empty to use the default set.
    Available: id, tracking_number, status, created, pickup_date, delivered_date,
    cash_amount, delivery_attempts, is_exchange, merchant_order_reference,
    customer_name, customer_phone, address, city, governorate.
    """
    try:
        orders = fetch_orders(
            status=status,
            status_except=status_except,
            tracking_number=tracking_number,
            phone=phone,
            merchant_order_reference=merchant_order_reference,
            is_exchange=is_exchange,
            delivery_attempts=delivery_attempts,
            cash_amount=cash_amount,
            cash_amount__gt=cash_amount__gt,
            created=created,
            pickup_date=pickup_date,
            delivered_date=delivered_date,
            city=city,
            governorate=governorate,
        )
        if not orders:
            return "No orders matched these filters, so no file was created."

        df = pd.DataFrame([flatten_order(o) for o in orders])

        target_columns = columns or DEFAULT_COLUMNS
        unknown = [c for c in target_columns if c not in df.columns]
        if unknown:
            return f"Unknown columns: {unknown}. Available: {list(df.columns)}"
        df = df[target_columns]

        EXPORTS_DIR.mkdir(exist_ok=True)
        path = EXPORTS_DIR / f"orders_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
        df.to_excel(path, index=False)

        return f"Done. {len(df)} orders exported with columns {target_columns}. File: {path.resolve()}"
    except requests.exceptions.HTTPError as e:
        return f"error {e.response.status_code}"

