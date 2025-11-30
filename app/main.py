from fastapi import Body, FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from zarinpal import ZarinPal
from zarinpal_utils. Config import Config as ZarinpalConfig

from app.database import engine, get_db
from app. models import Donation, Base
from app.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Donation App")

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_zarinpal():
    config = ZarinpalConfig(
        merchant_id=settings. zarinpal_merchant_id,
        sandbox=settings.zarinpal_sandbox
    )
    return ZarinPal(config)

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/total")
async def get_total(db: Session = Depends(get_db)):
    total = db.query(Donation). filter(Donation.status == "success").with_entities(
        func.sum(Donation.amount)
    ).scalar()
    return {"total": total or 0}

@app.post("/api/donate")
async def create_donation(amount: int = Body(...), db: Session = Depends(get_db)):
    if amount < 10000:
        raise HTTPException(status_code=400, detail="Minimum amount is 10000 Rials")
    
    try:
        zarinpal = get_zarinpal()
        
        response = zarinpal.payments.create({
            "amount": amount,
            "callback_url": settings.zarinpal_callback_url,
            "description": "کمک مالی"
        })
        
        if "data" in response and "authority" in response["data"]:
            authority = response["data"]["authority"]
            
            donation = Donation(
                authority=authority,
                amount=amount,
                status="pending"
            )
            db.add(donation)
            db.commit()
            
            payment_url = zarinpal.payments.generate_payment_url(authority)
            return {"payment_url": payment_url, "authority": authority}
        else:
            raise HTTPException(status_code=500, detail="Payment creation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/verify")
async def verify_payment(Authority: str, Status: str, db: Session = Depends(get_db)):
    donation = db.query(Donation). filter(Donation.authority == Authority).first()
    
    if not donation:
        return RedirectResponse(url="/? status=error&message=transaction_not_found")
    
    if Status != "OK":
        donation.status = "cancelled"
        db.commit()
        return RedirectResponse(url="/?status=error&message=cancelled")
    
    try:
        zarinpal = get_zarinpal()
        
        response = zarinpal.verifications.verify({
            "amount": donation.amount,
            "authority": Authority
        })
        
        if response["data"]["code"] in [100, 101]:
            donation.status = "success"
            donation.ref_id = str(response["data"]["ref_id"])
            donation.verified_at = datetime.utcnow()
            db.commit()
            
            return RedirectResponse(url=f"/?status=success&ref_id={donation.ref_id}")
        else:
            donation.status = "failed"
            db.commit()
            return RedirectResponse(url="/?status=error&message=verification_failed")
            
    except Exception as e:
        donation. status = "error"
        db.commit()
        return RedirectResponse(url=f"/?status=error&message={str(e)}")

from sqlalchemy import func
