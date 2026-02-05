from fastapi import HTTPException, Header
from typing import Optional
from config import config

def validate_api_key(api_key: Optional[str] = Header(None, alias="x-api-key")) -> str:
    # Temporarily disable API key for testing
    # if not config.API_KEY:
    #     raise HTTPException(status_code=500, detail="API key not configured")
    # 
    # if not api_key:
    #     raise HTTPException(status_code=401, detail="Missing API key")
    # 
    # if api_key != config.API_KEY:
    #     raise HTTPException(status_code=401, detail="Invalid API key")
    # 
    # return api_key
    
    # For testing - accept any key or no key
    return api_key or "test-key"
