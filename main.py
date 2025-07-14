from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PhoneLookupRequest(BaseModel):
    phone: str

class CustomerData(BaseModel):
    customer_id: str
    order_count_last_6m: int
    total_spend: float
    delivery_success_rate: float
    return_rate: float
    complaint_count: int
    avg_rating: float
    cod_attempts: int
    cod_failed: int
    address_changes: int

mock_db = {
    "01012345678": {
        "customer_id": "C1001",
        "order_count_last_6m": 12,
        "total_spend": 8500,
        "delivery_success_rate": 0.92,
        "return_rate": 0.05,
        "complaint_count": 1,
        "avg_rating": 4.2,
        "cod_attempts": 5,
        "cod_failed": 1,
        "address_changes": 2
    },
    "01123456789": {
        "customer_id": "C1002",
        "order_count_last_6m": 4,
        "total_spend": 1200,
        "delivery_success_rate": 0.75,
        "return_rate": 0.15,
        "complaint_count": 3,
        "avg_rating": 3.4,
        "cod_attempts": 3,
        "cod_failed": 2,
        "address_changes": 4
    }
}

@app.post("/api/lookup")
def lookup(data: PhoneLookupRequest):
    entry = mock_db.get(data.phone)
    if not entry:
        return {"error": "العميل غير موجود"}
    return entry

@app.post("/api/evaluate")
def evaluate(data: CustomerData):
    score = 0
    score += min(data.order_count_last_6m, 10) * 2
    score += min(data.total_spend / 1000, 10) * 1.5
    score += data.delivery_success_rate * 10
    score -= data.return_rate * 10
    score -= data.complaint_count * 2
    score += data.avg_rating
    score -= data.cod_failed * 3
    score -= data.address_changes

    level = "جيد جدًا" if score > 30 else "متوسط" if score > 15 else "ضعيف"
    risk = "منخفض" if score > 30 else "متوسط" if score > 15 else "مرتفع"

    return {"score": round(score, 2), "level": level, "risk": risk}
