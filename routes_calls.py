from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import CallSignal
from schemas import CallOfferSchema, CallAnswerSchema, CallCandidateSchema, CallSignalOut

router = APIRouter(prefix="/call", tags=["WebRTC Signaling"])


# ----- DB SESSION -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================
#   1) SEND OFFER
# ============================
@router.post("/offer", response_model=CallSignalOut)
def send_offer(data: CallOfferSchema, db: Session = Depends(get_db)):
    """
    Caller надсилає SDP-offer → записується сигнал у БД.
    """
    signal = CallSignal(
        from_id=data.from_id,
        to_id=data.to_id,
        type="offer",
        content=data.sdp,
        created_at=datetime.utcnow(),
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal


# ============================
#   2) SEND ANSWER
# ============================
@router.post("/answer", response_model=CallSignalOut)
def send_answer(data: CallAnswerSchema, db: Session = Depends(get_db)):
    """
    Callee надсилає SDP-answer → запис у БД.
    """
    signal = CallSignal(
        from_id=data.from_id,
        to_id=data.to_id,
        type="answer",
        content=data.sdp,
        created_at=datetime.utcnow(),
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal


# ============================
#   3) SEND ICE CANDIDATE
# ============================
@router.post("/candidate", response_model=CallSignalOut)
def send_candidate(data: CallCandidateSchema, db: Session = Depends(get_db)):
    """
    Обмін ICE кандидатами під час дзвінка.
    """
    signal = CallSignal(
        from_id=data.from_id,
        to_id=data.to_id,
        type="candidate",
        content=data.candidate,
        created_at=datetime.utcnow(),
    )
    db.add(signal)
    db.commit()
    db.refresh(signal)
    return signal


# ============================
#   4) GET SIGNALS (long polling)
# ============================
@router.get("/poll/{user_id}", response_model=list[CallSignalOut])
def poll_signals(user_id: int, db: Session = Depends(get_db)):
    """
    Клієнт періодично опитує цей endpoint.
    Повертаються всі сигналінг-повідомлення, адресовані user_id.
    Після видачі — вони видаляються з черги.
    """
    signals = (
        db.query(CallSignal)
        .filter(CallSignal.to_id == user_id)
        .order_by(CallSignal.created_at.asc())
        .all()
    )

    out = [s for s in signals]

    # Видаляємо з черги
    for s in signals:
        db.delete(s)
    db.commit()

    return out
