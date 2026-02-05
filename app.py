from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
from models import HoneypotRequest
from auth import validate_api_key
from handler import HoneypotHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Honeypot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

honeypot_handler = HoneypotHandler()

@app.post("/honeypot/message")
async def handle_honeypot_message(
    request: HoneypotRequest,
    api_key: str = Depends(validate_api_key)
):
    try:
        result = honeypot_handler.handle_message(request)
        return result
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
