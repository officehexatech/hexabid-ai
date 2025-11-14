from fastapi import APIRouter, HTTPException, Depends, status, Request, Response, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
import os
import httpx
from models import User, UserCreate, UserLogin, TokenResponse

router = APIRouter()
security = HTTPBearer(auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("JWT_SECRET", "hexabid-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
EMERGENT_AUTH_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

def get_db():
    from server import db
    return db

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_db)
) -> User:
    # Try session token from cookie first
    session_token = request.cookies.get("session_token")
    if session_token:
        session = await db.user_sessions.find_one({"session_token": session_token})
        if session and session.get("expires_at") > datetime.now(timezone.utc):
            user_doc = await db.users.find_one({"id": session["user_id"]}, {"_id": 0})
            if user_doc:
                if isinstance(user_doc.get('createdAt'), str):
                    user_doc['createdAt'] = datetime.fromisoformat(user_doc['createdAt'])
                return User(**user_doc)
    
    # Fallback to JWT token
    if credentials:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user_doc = await db.users.find_one({"id": user_id}, {"_id": 0})
        if user_doc is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        if isinstance(user_doc.get('createdAt'), str):
            user_doc['createdAt'] = datetime.fromisoformat(user_doc['createdAt'])
        return User(**user_doc)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Check if user exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        fullName=user_data.fullName,
        phone=user_data.phone
    )
    user_dict = user.model_dump()
    user_dict["hashedPassword"] = hash_password(user_data.password)
    user_dict["createdAt"] = user_dict["createdAt"].isoformat()
    
    await db.users.insert_one(user_dict)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(accessToken=access_token, user=user)

@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    # Find user
    user_doc = await db.users.find_one({"email": login_data.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Verify password
    if not verify_password(login_data.password, user_doc.get("hashedPassword", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Parse datetime
    if isinstance(user_doc.get('createdAt'), str):
        user_doc['createdAt'] = datetime.fromisoformat(user_doc['createdAt'])
    
    user = User(**user_doc)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(accessToken=access_token, user=user)

@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/google/session")
async def process_google_session(
    response: Response,
    x_session_id: str = Header(..., alias="X-Session-ID"),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Process Emergent Auth session ID and create user session"""
    try:
        # Get user data from Emergent Auth
        async with httpx.AsyncClient() as client:
            auth_response = await client.get(
                EMERGENT_AUTH_URL,
                headers={"X-Session-ID": x_session_id},
                timeout=10.0
            )
            auth_response.raise_for_status()
            auth_data = auth_response.json()
        
        # Extract user data
        user_email = auth_data.get("email")
        user_name = auth_data.get("name")
        user_picture = auth_data.get("picture")
        session_token = auth_data.get("session_token")
        
        if not user_email or not session_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session data")
        
        # Check if user exists
        existing_user = await db.users.find_one({"email": user_email}, {"_id": 0})
        
        if existing_user:
            user = User(**existing_user)
        else:
            # Create new user
            user = User(
                email=user_email,
                fullName=user_name,
                googleId=auth_data.get("id")
            )
            user_dict = user.model_dump()
            user_dict["createdAt"] = user_dict["createdAt"].isoformat()
            await db.users.insert_one(user_dict)
        
        # Store session in database
        session_doc = {
            "user_id": user.id,
            "session_token": session_token,
            "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
            "created_at": datetime.now(timezone.utc)
        }
        await db.user_sessions.insert_one(session_doc)
        
        # Set httpOnly cookie
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=7 * 24 * 60 * 60,  # 7 days
            path="/"
        )
        
        return {
            "success": True,
            "user": user,
            "message": "Authentication successful"
        }
        
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to authenticate with Google: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}"
        )

@router.post("/logout")
async def logout(response: Response, request: Request, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Logout user and clear session"""
    session_token = request.cookies.get("session_token")
    
    if session_token:
        # Delete session from database
        await db.user_sessions.delete_one({"session_token": session_token})
    
    # Clear cookie
    response.delete_cookie(key="session_token", path="/")
    
    return {"message": "Logged out successfully"}