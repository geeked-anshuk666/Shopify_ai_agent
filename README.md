# Shopify AI Agent

A robust, full-stack AI application designed to analyze Shopify store data using a LangChain-powered agent. This tool empowers store owners to query their data (Orders, Products, Customers) using natural language, providing actionable insights, tabular summaries, and business recommendations.

## 🚀 Features

-   **Natural Language Querying**: Ask questions like "How many orders were placed in the last 7 days?" or "Who are my top customers?".
-   **Intelligent Analysis**: Leverages Google's Gemini Pro via LangChain to interpret data and generate strategic insights.
-   **Automated Data Retrieval**: Custom-built tool to securely fetch data from Shopify Admin REST API (GET-only).
-   **Robust Error Handling**: Handles API rate limits (HTTP 429), pagination, and malformed data gracefully.
-   **Secure**: Strictly read-only operations; checks prevent unsafe actions (POST/PUT/DELETE).
-   **Modern UI**: Clean, responsive React frontend with Markdown and Table rendering support.

## 🏗 Architecture

The application follows a decoupled client-server architecture:

### Backend (`/backend`)
-   **Framework**: FastAPI (Python) for high-performance Async I/O.
-   **AI Orchestration**: LangChain (ReAct Agent pattern) manages the reasoning loop.
-   **LLM**: Google Gemini Pro (via `langchain-google-genai`).
-   **Tools**:
    -   `get_shopify_data`: A resilient wrapper around `requests` that handles Shopify's cursor-based pagination and leaky bucket rate limiting using `tenacity`.
    -   `PythonREPLAst`: Allows the agent to perform complex data aggregations and filtering using Pandas.

### Frontend (`/frontend`)
-   **Framework**: React (Vite).
-   **Styling**: Tailwind CSS for a professional, responsive design.
-   **Components**: Custom Chat Interface with `react-markdown` to render rich text and data tables.

## 🛠 Prerequisites

-   Python 3.9+
-   Node.js 18+
-   Shopify Store Credentials (Shop URL, Access Token)
-   Google Gemini API Key

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd shopify-ai-agent
```

### 2. Backend Setup

Navigate to the backend directory and set up the Python environment.

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Environment Variables**:
Create a `.env` file in the root `backend` directory (or leverage the provided one in root if running from there).

```env
SHOPIFY_SHOP_NAME="your-shop.myshopify.com"
SHOPIFY_ACCESS_TOKEN="your_shpat_token"
SHOPIFY_API_VERSION="2025-07"
GOOGLE_API_KEY="your_gemini_api_key"
```

### 3. Frontend Setup

Navigate to the frontend directory.

```bash
cd ../frontend
npm install
```

## 🚀 Running the Application

### Start the Backend Server

From the `backend` directory (with venv activated):

```bash
python main.py
```
The API will start at `http://localhost:8000`.

### Start the Frontend Client

From the `frontend` directory:

```bash
npm run dev
```
The application will be accessible at `http://localhost:5173`.

## 🧪 Usage Examples

Once the application is running, try asking:

1.  **Sales Analysis**: "How many orders did we get in the last 7 days?"
2.  **Product Insights**: "Which products are top sellers this month?"
3.  **Customer Data**: "List customers who ordered more than 3 times."
4.  **Strategic Advice**: "What is the AOV trend this month?"

## 🛡 Security & Best Practices

-   **Least Privilege**: The Shopify API token should only have `read_orders`, `read_products`, and `read_customers` scopes.
-   **Input Validation**: All agent inputs and tool outputs are sanitized.
-   **Environment Isolation**: Secrets are never committed to code (handled via `.env` and `.gitignore`).
-   **Rate Limiting**: Implemented exponential backoff for API stability.

## 📝 Known Issues / Limitations

-   Charts are currently described textually or in tabular format. Visual chart rendering is a planned future enhancement.
-   Large datasets (>1000 records) are capped for performance in this demonstration.

## 📄 License

[MIT License](LICENSE)
