import logging
from app.models.market_price import MarketPrice

logger = logging.getLogger(__name__)

def calculate_financials(predicted_yield_t_ha: float, farm_size_acres: float, fertilizer_kg: float, pesticide_kg: float) -> dict:
    """
    Calculates Expected Production, Gross Revenue, Input Costs, and Net Profit.
    Queries the database dynamically for the latest admin-updated market price.
    """
    try:
        # Default fallback price if DB query fails or table is empty
        price_per_ton = 18500.0 
        
        try:
            # Attempt to fetch dynamic price from the database
            price_record = MarketPrice.query.filter_by(crop_name='Rice').first()
            if price_record:
                price_per_ton = price_record.price_per_ton
        except Exception as db_err:
            logger.warning(f"Could not fetch MarketPrice from DB, using fallback: {db_err}")

        # Convert Acres to Hectares (1 Acre = 0.404686 Hectares)
        area_ha = farm_size_acres * 0.404686
        
        # Total Production in Tons
        total_production = predicted_yield_t_ha * area_ha
        
        # Gross Revenue
        gross_revenue = total_production * price_per_ton
        
        # Estimate Input Costs (Approximations for simulation purposes)
        cost_fert = fertilizer_kg * 30.0  # ₹30 per kg of fertilizer
        cost_pest = pesticide_kg * 800.0  # ₹800 per kg of pesticide
        cost_labor = farm_size_acres * 5000.0 # ₹5000 per acre for labor/machinery
        
        total_cost = cost_fert + cost_pest + cost_labor
        
        # Net Profit
        expected_profit = gross_revenue - total_cost

        return {
            "predicted_yield_t_ha": round(predicted_yield_t_ha, 2),
            "total_production_tons": round(total_production, 2),
            "market_price_per_ton": round(price_per_ton, 2),
            "gross_revenue_inr": round(gross_revenue, 2),
            "input_cost_inr": round(total_cost, 2),
            "expected_profit_inr": round(expected_profit, 2)
        }
        
    except Exception as e:
        logger.error(f"Error calculating financials: {e}")
        return {
            "predicted_yield_t_ha": round(predicted_yield_t_ha, 2),
            "total_production_tons": 0.0,
            "market_price_per_ton": 0.0,
            "gross_revenue_inr": 0.0,
            "input_cost_inr": 0.0,
            "expected_profit_inr": 0.0
        }