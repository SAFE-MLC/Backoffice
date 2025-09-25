import jwt
from datetime import datetime, timedelta, timezone
from config import SESSION_KEY

def generar_session_token(ticket_id: str, minutes_valid: int = 10):
    now = datetime.now(timezone.utc)
    exp_time = now + timedelta(minutes=minutes_valid)
    payload = {
        "sub": ticket_id,
        "iat": now,
        "exp": exp_time,
    }
    token = jwt.encode(payload, SESSION_KEY, algorithm="HS256")
    return token, exp_time

