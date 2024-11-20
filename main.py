from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

# 업비트 API 기본 URL
UPBIT_API_BASE = "https://api.upbit.com/v1"

# Pydantic 모델 정의
class Market(BaseModel):
    market: str
    korean_name: str
    english_name: str

class Ticker(BaseModel):
    market: str
    trade_date: str
    trade_time: str
    trade_price: float
    change: str
    change_price: float
    high_price: float
    low_price: float
    timestamp: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Upbit API FastAPI service!"}

@app.get("/markets", response_model=list[Market])
async def get_markets():
    """
    업비트에서 지원하는 마켓 정보를 가져옵니다.
    """
    url = f"{UPBIT_API_BASE}/market/all"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # HTTP 에러가 발생하면 예외를 던짐
            data = response.json()
            return data
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {e}")

@app.get("/ticker/{market}", response_model=list[Ticker])
async def get_ticker(market: str):
    """
    특정 시장(market)의 현재 가격 정보를 가져옵니다.
    """
    url = f"{UPBIT_API_BASE}/ticker?markets={market}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            return data
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=response.status_code, detail=f"HTTP error: {e}")
