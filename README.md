# MCP Inventory Optimization Server

A Model Context Protocol (MCP) server that provides inventory optimization tools for supply chain management. This server implements two key tools for inventory optimization: safety stock calculation and lead time simulation.

## Features

- **Safety Stock Optimization**: Calculate optimal safety stock levels based on historical demand data fetched from an external API
- **Lead Time Simulation**: Simulate inventory levels over time based on lead times and demand patterns

## Prerequisites

- Python 3.13 or higher
- UV (Python package installer)
- Access to historical data API (running on https://localhost:8003)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-erp
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies using UV:
```bash
uv pip install -e .
```

## Usage

1. Ensure the historical data API is running on https://localhost:8003

2. Start the MCP server:
```bash
python server.py
```

3. The server exposes two tools that can be used by any MCP client:

### 1. Optimize Safety Stock

Calculates optimal safety stock levels based on historical demand data fetched from an external API.

Parameters:
- `item_id` (str): Unique identifier for the item
- `desired_service_level` (float): Target service level (0-1)

Example input:
```python
{
    "item_id": "ITEM001",
    "desired_service_level": 0.95
}
```

The function will:
1. Fetch historical data from https://localhost:8003/histdata/{item_id}
2. Calculate safety stock using statistical methods
3. Return the results including:
   - Calculated safety stock level
   - Average demand
   - Standard deviation of demand
   - Number of data points used

### 2. Simulate Lead Time

Simulates inventory levels over time based on lead times and demand patterns.

Parameters:
- `item_id` (str): Unique identifier for the item
- `lead_times` (List[int]): List of historical lead times in days
- `demand_data` (List[Dict]): List of daily demand records with 'date' and 'quantity' fields

Example input:
```python
{
    "item_id": "ITEM001",
    "lead_times": [5, 7, 6, 8, 5],
    "demand_data": [
        {"date": "2024-01-01", "quantity": 10},
        {"date": "2024-01-02", "quantity": 15},
        # ... more demand data
    ]
}
```

## Development

The server is built using the MCP Python SDK and implements two async tool functions:

1. `optimize_safety_stock`: Fetches historical data from an external API and calculates safety stock using statistical methods
2. `simulate_lead_time`: Simulates inventory levels over a 30-day period

### Project Structure

```
mcp-erp/
├── server.py          # Main server implementation
├── pyproject.toml     # Project dependencies
├── uv.lock           # UV lock file for dependency versions
└── README.md         # This file
```

## Dependencies

- mcp[cli]>=1.9.1: MCP Python SDK
- numpy>=1.24.0: For statistical calculations
- aiohttp>=3.9.0: For async HTTP requests
- certifi: For SSL certificate verification

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
