import os
from typing import Optional

class Config:
    API_KEY: Optional[str] = os.getenv("API_KEY") or "test-key-12345"  # Default for testing
    GUVI_CALLBACK_URL: str = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    MAX_MESSAGES: int = 15
    MAX_NO_NEW_INTEL: int = 3

config = Config()
