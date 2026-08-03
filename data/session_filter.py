from datetime import datetime, timezone, timedelta
from core_layer.logger.logger import setup_logger

logger = setup_logger("SessionFilter")

# Tashkent is UTC+5 year-round (no Daylight Saving Time)
TASHKENT_TZ = timezone(timedelta(hours=5))

def get_tashkent_time() -> datetime:
    """
    Returns the current timezone-aware datetime in Tashkent (UTC+5).
    """
    return datetime.now(timezone.utc).astimezone(TASHKENT_TZ)

def is_trading_time() -> bool:
    """
    Evaluates if the current Tashkent time falls within active trading parameters:
    Monday-Friday, 08:00 to 23:59.
    """
    tashkent_now = get_tashkent_time()
    
    # Python weekday(): 0 = Monday, 1 = Tuesday, ..., 4 = Friday, 5 = Saturday, 6 = Sunday
    is_weekday = tashkent_now.weekday() < 5
    
    # Trading window: 08:00 to 23:59 means the hour must be 8 or greater.
    is_active_hour = tashkent_now.hour >= 8
    
    if is_weekday and is_active_hour:
        return True
        
    logger.info(f"Outside trading hours, skipping. Current Tashkent time: {tashkent_now.strftime('%A, %Y-%m-%d %H:%M:%S')}")
    return False
