import random
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Secret token
SECRET_TOKEN = "BUWE8374324234324324"

class Message(BaseModel):
    atlpSubmissionID: str
    jobType: str
    jobOrderNumber: str

ID = "ID"

def generate_message_id():
    random_number = random.randint(1000000, 9999999)  # Generate random 7-digit number
    return f"{ID}{random_number}"

def verify_token(token: Optional[str] = None):
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/MockServerTest")
async def process_message(
    message: Message,
    request: Request,
    token: Optional[str] = Header(None),
    authorization: str = Header(None),
    content_type: str = Header(None),
):
    if authorization:
        verify_token(authorization)
    elif token:
        verify_token(token)
    else:
        raise HTTPException(status_code=401, detail="Missing token")
    
    message_id = generate_message_id()
    
    # Accessing headers
    #headers = dict(request.headers)
    #print("Headers:", headers)
    
    return {
        "message_id": message_id,
        "status": "success",
        "message": message.dict(),
        "authorization_header": authorization,
        "token_header": token,
        "content_type_header": content_type
    }

# Run uvicorn main:app --port 1406 --reload to start the server




