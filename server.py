from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
import numpy as np
from datetime import datetime, timedelta
import aiohttp
import ssl
import certifi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("Inventory Optimization Server")

@mcp.tool()
async def optimize_safety_stock(item_id: str, desired_service_level: float) -> Dict[str, Any]:
    """
    Calculate optimal safety stock level based on historical data and desired service level.
    Historical data is fetched from an external API.
    
    Args:
        item_id: Unique identifier for the item
        desired_service_level: Target service level (0-1)
    
    Returns:
        Dictionary containing safety stock calculation results
    """
    # Create SSL context for HTTPS request
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    
    # Fetch historical data from external API
    async with aiohttp.ClientSession() as session:
        try:
            logger.info(f"Fetching historical data for item {item_id}")
            async with session.get(
                f"https://gs3z7pyxxc.execute-api.eu-west-1.amazonaws.com/default/mcp-erp-poc"
            ) as response:
                if response.status != 200:
                    error_msg = f"Failed to fetch historical data: HTTP {response.status}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                historical_data = await response.json()
                logger.info(f"Received {len(historical_data)} data points for item {item_id}")
                
                if not historical_data:
                    error_msg = "No historical data received from API"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
                # Process the data
                try:
                    # Extract quantities from the historical data
                    # The API returns data in the format: [{"date": "2024-01-01", "demand": 10}, ...]
                    demands = [record['demand'] for record in historical_data]
                    
                    if not demands:
                        error_msg = "No demand data found in historical records"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                    
                    avg_demand = np.mean(demands)
                    std_demand = np.std(demands)
                    
                    # Simple safety stock calculation using normal distribution
                    z_score = 1.96  # For 95% service level
                    safety_stock = z_score * std_demand
                    
                    result = {
                        "item_id": item_id,
                        "safety_stock": round(safety_stock, 2),
                        "average_demand": round(avg_demand, 2),
                        "std_demand": round(std_demand, 2),
                        "service_level": desired_service_level,
                        "data_points": len(historical_data)
                    }
                    logger.info(f"Successfully calculated safety stock for item {item_id}: {result}")
                    return result
                    
                except KeyError as e:
                    error_msg = f"Invalid data format in historical records: {str(e)}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                except Exception as e:
                    error_msg = f"Error processing historical data: {str(e)}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                
        except aiohttp.ClientError as e:
            error_msg = f"Error connecting to historical data API: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

@mcp.tool()
async def simulate_lead_time(item_id: str, lead_times: List[int], demand_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Simulate inventory levels based on lead times and demand data.
    
    Args:
        item_id: Unique identifier for the item
        lead_times: List of historical lead times in days
        demand_data: List of daily demand records with 'date' and 'quantity' fields
    
    Returns:
        Dictionary containing simulation results
    """
    # Mock implementation
    avg_lead_time = np.mean(lead_times)
    std_lead_time = np.std(lead_times)
    
    # Simulate 30 days of inventory
    start_date = datetime.now()
    simulation_days = 30
    daily_demands = [record['quantity'] for record in demand_data]
    avg_daily_demand = np.mean(daily_demands)
    
    # Generate simulated inventory levels
    inventory_levels = []
    current_inventory = 100  # Starting inventory
    
    for day in range(simulation_days):
        # Simulate daily demand
        daily_demand = np.random.normal(avg_daily_demand, np.std(daily_demands))
        current_inventory -= daily_demand
        
        # Simulate replenishment if inventory is low
        if current_inventory < 20:
            current_inventory += 100  # Replenishment quantity
        
        inventory_levels.append({
            "date": (start_date + timedelta(days=day)).isoformat(),
            "inventory_level": round(current_inventory, 2)
        })
    
    return {
        "item_id": item_id,
        "average_lead_time": round(avg_lead_time, 2),
        "std_lead_time": round(std_lead_time, 2),
        "simulation_results": inventory_levels
    }

if __name__ == "__main__":
    mcp.run()
