# 🚚 Delivery Operations AI Agent

An intelligent, conversational operations assistant designed to automate delivery order tracking, logistics management, analytics, and report generation for delivery and transportation networks.

Powered by **LangGraph**, **LangChain**, and **Google Gemini**, this agent understands natural language queries in both **Arabic** and **English**, interacts directly with the delivery operations REST API, and can generate and export customized Excel reports on demand.

---

## ✨ Features

- **Natural Language Querying (Arabic & English):** Ask questions conversationally like *"كام شحنة مرتجعة في الجيزة؟"* or *"Show me all delivered orders from yesterday"*.
- **Live Logistics API Integration:** Seamlessly retrieves real-time order data, tracking lifecycles, customer details, and cash-on-delivery (COD) records.
- **Automated Pagination & Location Filtering:** Traverses multi-page API results and supports deep filtering by status, governorate, city, delivery attempts, and dates.
- **Instant Excel Report Generation:** Automatically creates formatted `.xlsx` spreadsheets in `exports/` tailored to specific filter criteria and requested columns.
- **Robust Error Handling:** Detects missing orders, handles API faults, and prevents invalid parameter lookups.
- **Clean Modular Architecture:** Structured according to clean code principles with clear separation of concerns and zero clutter.

---

## 🏗️ Architecture

```
Transportation Agent/
├── config.py           # Environment loading, API keys, headers, and defaults
├── api_client.py       # Delivery API client with cursor pagination & nested filtering
├── utils.py            # Data extraction, summarization, and dictionary flattening
├── tools.py            # LangChain agent tools (get_order, list_orders, export_orders_to_excel)
├── prompts.py          # Dynamic system prompt with date injection and operational rules
├── agent.py            # LLM initialization and LangGraph ReAct Agent builder
├── main.py             # CLI entrypoint for interactive chat or one-off queries
├── exports/            # Storage directory for generated Excel spreadsheets
├── .env                # Environment secrets (API keys and endpoints)
└── test.ipynb          # Exploratory notebook
```

### Module Responsibilities

| Module | Responsibility |
| :--- | :--- |
| **`config.py`** | Centralizes configuration, environment loading (`.env`), and constants like `BASE_URL` and `DEFAULT_COLUMNS`. |
| **`api_client.py`** | Low-level HTTP requests to delivery endpoints (`/delivery-orders/`), handling cursor pagination, headers, and post-filtering. |
| **`utils.py`** | Pure helper utilities: `get_nested` for safe dictionary traversing, `summarize` for compact records, and `flatten_order` for table tabularization. |
| **`tools.py`** | Exposes `@tool` wrappers with strict schema docstrings for the LLM agent to execute actions safely. |
| **`prompts.py`** | Houses the `SYSTEM_PROMPT` ensuring strict groundedness (no hallucinations), Arabic localization, and tool selection instructions. |
| **`agent.py`** | Configures `ChatGoogleGenerativeAI` and builds the LangGraph ReAct agent. |
| **`main.py`** | Terminal interface supporting both an interactive REPL loop and direct command-line arguments. |

---

## 🛠️ Tools Available to the Agent

The agent is equipped with three core tools:

1. **`get_order`**: Fetches full details for a single delivery order using its numerical `order_id` (package info, merchant details, timeline, and customer address).
2. **`list_orders`**: Retrieves orders matching specific filters (status, date, cash amount, delivery attempts, exchange, location). Automatically returns aggregates and statistics when results exceed 50 items.
3. **`export_orders_to_excel`**: Queries matching records, structures them into a Pandas DataFrame, and saves them directly to an Excel file in `exports/`, returning the absolute file path.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10+
- A Google Gemini API Key
- Delivery API backend credentials (or a running local delivery API server)

### 2. Installation

Clone or open the project directory and activate your virtual environment:

```bash
# Create and activate virtual environment (optional if using existing venv)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS / Linux

# Install dependencies
pip install requests pandas openpyxl python-dotenv langchain-classic langchain-google-genai langgraph
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
DELIVERY_API_BASE_URL="http://localhost:8000/api/v1"
DELIVERY_API_KEY="test-key"
GOOGLE_API_KEY="your-google-gemini-api-key"
```

---

## 💻 Usage

### Interactive Chat Mode

Launch the interactive assistant in your terminal:

```bash
python main.py
```

```text
You: كام شحنة مرتجعة عندنا؟
Agent: في 25 شحنة مرتجعة (returned).

You: هاتلي شيت بالمرتجعات في الجيزة، فيه الاسم والمدينة بس
Agent: تم تصدير 5 شحنات إلى ملف إكسيل بالأعمدة المطلوبة:
File: C:\Users\...\Transportation Agent\exports\orders_20261020_151000.xlsx

You: exit
```

### One-Off Command Line Queries

Pass your prompt directly as command-line arguments:

```bash
python main.py "هاتلي تفاصيل الشحنة SB931446384"
```

```bash
python main.py "What is the total cash collected for delivered orders in Cairo?"
```

---

## 📊 Excel Export Columns

When exporting to Excel via `export_orders_to_excel`, the following default columns are included unless specified otherwise:

- `tracking_number`
- `status`
- `created`
- `delivered_date`
- `cash_amount`
- `customer_name`
- `customer_phone`
- `city`
- `governorate`

Additional columns available: `id`, `pickup_date`, `delivery_attempts`, `is_exchange`, `merchant_order_reference`, and `address`.

---

## 🔒 Best Practices & Reliability

- **Zero Hallucination Policy:** The system prompt explicitly enforces answering strictly from tool outputs.
- **Accurate Keyword Argument Binding:** All internal tool-to-client invocations use explicit named arguments to eliminate positional parameter errors.
- **Graceful Error Handling:** HTTP 404 and API failures are translated into user-friendly messages rather than crashing the agent execution loop.
