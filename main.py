from fastapi import FastAPI, Query
from pydantic import BaseModel, EmailStr
import dns.resolver
import socket

app = FastAPI()

DISPOSABLE_DOMAINS = {"mailinator.com", "tempmail.com", "10minutemail.com"}

class ValidationResult(BaseModel):
    email: EmailStr
    valid_syntax: bool
    has_mx: bool
    is_disposable: bool

def has_mx_record(domain: str) -> bool:
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except:
        return False

def is_disposable_email(domain: str) -> bool:
    return domain.lower() in DISPOSABLE_DOMAINS

@app.get("/validate", response_model=ValidationResult)
def validate_email(email: str = Query(...)):
    valid_syntax = True
    try:
        local_part, domain = email.split("@")
        has_mx = has_mx_record(domain)
        is_disposable = is_disposable_email(domain)
    except Exception:
        valid_syntax = False
        has_mx = False
        is_disposable = False

    return {
        "email": email,
        "valid_syntax": valid_syntax,
        "has_mx": has_mx,
        "is_disposable": is_disposable
    }
