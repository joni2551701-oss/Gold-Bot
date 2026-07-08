import os
from datetime import timezone

class Config:
    # ... mavjud sozlamalar ...
    
    # Timeframe fetching configuration
    TIMEFRAME_HISTORY = {
        "M5": 200,
        "M15": 200,
        "H1": 200,
        "H4": 100
    }
