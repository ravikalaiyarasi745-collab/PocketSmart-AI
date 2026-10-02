# PocketSmart AI — Complete Source Code

Each section is one file. Create the folders shown in each heading, then paste the code into that file.

## `.env.example`

```dotenv
APP_NAME=PocketSmart AI
ENVIRONMENT=development
SECRET_KEY=replace-this-with-a-long-random-secret
DATABASE_URL=sqlite:///./pocketsmart.db
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
MOCK_AI=false
COOKIE_SECURE=false
ACCESS_TOKEN_EXPIRE_MINUTES=1440
MAX_UPLOAD_MB=5
CORS_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
```

## `.gitignore`

```text
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
.env
*.db
*.sqlite
*.sqlite3
.vscode/
.DS_Store
```

## `Dockerfile`

```text
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## `README.md`

```markdown
# PocketSmart AI

A complete FastAPI + Jinja2 + Gemini application for budget-aware recommendations across:

- Home interior planning
- Party/event planning
- Jewelry recommendations with optional outfit-image analysis
- User registration/login
- JWT authentication
- Recommendation history
- Deterministic mock catalog fallbacks when Gemini or live commerce APIs are unavailable

> The project documentation mentions Gemini 1.5 Flash Pro. That model name is configurable here through `GEMINI_MODEL`; the default is `gemini-2.5-flash` so the application is aligned with the current Google GenAI SDK. You can change it without modifying code.

## 1. Requirements

- Python 3.11+
- A Gemini API key for live AI recommendations
- VS Code (recommended)

The application works without a Gemini key in `MOCK_AI=true` mode, which is useful for frontend/backend testing.

## 2. Project structure

```text
PocketSmartAI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── schemas.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── recommendations.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py
│   │   ├── mock_catalog.py
│   │   └── recommendation_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── planner.html
│   │   └── recommendations.html
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── run.py
```

## 3. VS Code setup

### Windows PowerShell

```powershell
cd PocketSmartAI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

### macOS/Linux

```bash
cd PocketSmartAI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=your_key_here
```

For testing without Gemini:

```env
MOCK_AI=true
```

## 4. Run

```bash
python run.py
```

Open:

http://127.0.0.1:8000

Or:

```bash
uvicorn app.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

## 5. Test

```bash
pytest -q
```

The test suite exercises registration, login, session information, planner APIs, history, and mock-AI behavior.

## 6. Gemini configuration

`.env`:

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
MOCK_AI=false
```

The jewelry endpoint accepts an optional image. The image is validated in the API and sent to Gemini as multimodal input; it is not permanently stored by the application.

## 7. Commerce/service data

The supplied project documentation calls for Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO and similar sources, and explicitly permits mock/simulated calls. This implementation uses a deterministic local catalog instead of scraping those sites. It generates safe search links rather than pretending that a particular live product price or inventory was verified.

To integrate real APIs later, replace `app/services/mock_catalog.py` with provider adapters and keep the recommendation service interface unchanged.

## 8. Production notes

Before production:

- Use PostgreSQL instead of SQLite.
- Put the app behind HTTPS.
- Store `SECRET_KEY` and `GEMINI_API_KEY` in a secret manager.
- Set `COOKIE_SECURE=true`.
- Add rate limiting and request logging.
- Add CSRF protection if you change the authentication flow to cookie-only state-changing forms.
- Add provider APIs or a compliant product-data service instead of scraping commerce websites.
- Review Gemini safety, privacy, retention, and regional requirements for your deployment.
```

## `app/__init__.py`

```python

```

## `app/config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    environment: str = "development"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./pocketsmart.db"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    mock_ai: bool = False
    cookie_secure: bool = False
    access_token_expire_minutes: int = 1440
    max_upload_mb: int = 5
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

## `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings

settings = get_settings()

connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## `app/dependencies.py`

```python
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Cookie, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from .config import get_settings
from .database import get_db
from .models.db import User

settings = get_settings()
ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def _decode(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )


def get_current_user(
    authorization: str | None = Header(default=None),
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    token = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
    elif access_token:
        token = access_token

    if not token:
        raise HTTPException(status_code=401, detail="Authentication required")

    user = db.get(User, _decode(token))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)
```

## `app/main.py`

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import Base, engine
from .routes.auth import router as auth_router
from .routes.pages import router as pages_router
from .routes.recommendations import router as recommendation_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    description="Budget-aware GenAI recommendation assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(recommendation_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}
```

## `app/models/__init__.py`

```python

```

## `app/models/db.py`

```python
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    recommendations: Mapped[list["RecommendationHistory"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    planner: Mapped[str] = mapped_column(String(30), index=True)
    budget: Mapped[float] = mapped_column()
    input_json: Mapped[str] = mapped_column(Text)
    result_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    user: Mapped[User] = relationship(back_populates="recommendations")
```

## `app/models/schemas.py`

```python
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1)
    style: str = Field(default="modern", max_length=100)
    notes: str = Field(default="", max_length=1000)
    items: dict[str, int] = Field(default_factory=dict)


class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=100)
    venue: str = Field(default="flexible", max_length=200)
    notes: str = Field(default="", max_length=1000)


class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="elegant", max_length=100)
    metal: str = Field(default="any", max_length=50)
    notes: str = Field(default="", max_length=1000)


class RecommendationItem(BaseModel):
    category: str
    name: str
    platform: str
    estimated_price: float = Field(ge=0)
    reason: str
    search_url: str = ""


class RecommendationResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    budget: float
    total_estimated: float
    budget_remaining: float
    summary: str
    allocations: dict[str, float]
    recommendations: list[RecommendationItem]
    source_mode: str
    model: str | None = None
    model_config = ConfigDict(extra="allow")


class HistoryItem(BaseModel):
    id: int
    planner: str
    budget: float
    created_at: str
    result: dict[str, Any]
```

## `app/routes/__init__.py`

```python

```

## `app/routes/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from ..config import get_settings
from ..database import get_db
from ..dependencies import create_access_token, get_current_user, verify_password
from ..models.db import User
from ..models.schemas import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])
settings = get_settings()


@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest, response: Response, db: Session = Depends(get_db)):
    email = data.email.lower()
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(status_code=409, detail="Email is already registered")

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=generate_password_hash(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id)
    response.set_cookie(
        "access_token", token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == data.email.lower()))
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id)
    response.set_cookie(
        "access_token", token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"id": user.id, "name": user.name, "email": user.email}
```

## `app/routes/pages.py`

```python
import json

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models.db import RecommendationHistory

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="app/templates")


def optional_user(request: Request, db: Session):
    try:
        return get_current_user(
            authorization=request.headers.get("authorization"),
            access_token=request.cookies.get("access_token"),
            db=db,
        )
    except Exception:
        return None


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "user": optional_user(request, db)})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "user": None})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        user = optional_user(request, db)
        if not user:
            return RedirectResponse("/login", status_code=303)
        recent = db.scalars(
            select(RecommendationHistory)
            .where(RecommendationHistory.user_id == user.id)
            .order_by(RecommendationHistory.created_at.desc())
            .limit(6)
        ).all()
        return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "recent": recent})
    except Exception:
        return RedirectResponse("/login", status_code=303)


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request, db: Session = Depends(get_db)):
    user = optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    rows = db.scalars(
        select(RecommendationHistory)
        .where(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())
    ).all()
    return templates.TemplateResponse("history.html", {"request": request, "user": user, "rows": rows})


@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner_page(planner: str, request: Request, db: Session = Depends(get_db)):
    if planner not in {"home", "party", "jewelry"}:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(
        "planner.html",
        {"request": request, "user": optional_user(request, db), "planner": planner},
    )


@router.get("/recommendations/{history_id}", response_class=HTMLResponse)
def recommendations_page(history_id: int, request: Request, db: Session = Depends(get_db)):
    user = optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    row = db.get(RecommendationHistory, history_id)
    if not row or row.user_id != user.id:
        return RedirectResponse("/history", status_code=303)
    result = json.loads(row.result_json)
    return templates.TemplateResponse(
        "recommendations.html",
        {"request": request, "user": user, "history": row, "result": result},
    )
```

## `app/routes/recommendations.py`

```python
import json
from datetime import timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models.db import RecommendationHistory, User
from ..models.schemas import HomeRequest, JewelryRequest, PartyRequest, RecommendationResponse
from ..services.recommendation_service import recommend

router = APIRouter(prefix="/api", tags=["recommendations"])


def save_history(db: Session, user: User, planner: str, budget: float, payload: dict, result: dict):
    row = RecommendationHistory(
        user_id=user.id,
        planner=planner,
        budget=budget,
        input_json=json.dumps(payload, ensure_ascii=False),
        result_json=json.dumps(result, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.post("/generate-home", response_model=RecommendationResponse)
def generate_home(data: HomeRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    payload = data.model_dump()
    result = recommend("home", data.budget, payload)
    save_history(db, user, "home", data.budget, payload, result)
    return {"planner": "home", "budget": data.budget, **result}


@router.post("/generate-party", response_model=RecommendationResponse)
def generate_party(data: PartyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    payload = data.model_dump()
    result = recommend("party", data.budget, payload)
    save_history(db, user, "party", data.budget, payload, result)
    return {"planner": "party", "budget": data.budget, **result}


@router.post("/generate-jewelry", response_model=RecommendationResponse)
async def generate_jewelry(
    budget: float = Form(..., gt=0, le=10_000_000),
    occasion: str = Form(..., min_length=2, max_length=100),
    style: str = Form("elegant", max_length=100),
    metal: str = Form("any", max_length=50),
    notes: str = Form("", max_length=1000),
    outfit_image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    image_bytes = None
    mime_type = None

    if outfit_image:
        allowed = {"image/jpeg", "image/png", "image/webp"}
        if outfit_image.content_type not in allowed:
            raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WEBP images are supported")
        image_bytes = await outfit_image.read()
        max_bytes = 5 * 1024 * 1024
        if len(image_bytes) > max_bytes:
            raise HTTPException(status_code=413, detail="Image is too large; maximum is 5 MB")
        mime_type = outfit_image.content_type

    payload = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "metal": metal,
        "notes": notes,
        "image_attached": bool(image_bytes),
    }
    result = recommend("jewelry", budget, payload, image_bytes=image_bytes, mime_type=mime_type)
    save_history(db, user, "jewelry", budget, payload, result)
    return {"planner": "jewelry", "budget": budget, **result}


@router.get("/history")
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.scalars(
        select(RecommendationHistory)
        .where(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())
    ).all()
    return [
        {
            "id": row.id,
            "planner": row.planner,
            "budget": row.budget,
            "created_at": row.created_at.isoformat(),
            "result": json.loads(row.result_json),
        }
        for row in rows
    ]


@router.get("/recommendations-details/{history_id}")
def recommendation_details(
    history_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = db.get(RecommendationHistory, history_id)
    if not row or row.user_id != user.id:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {
        "id": row.id,
        "planner": row.planner,
        "budget": row.budget,
        "input": json.loads(row.input_json),
        "result": json.loads(row.result_json),
    }


@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"authenticated": True, "user_id": user.id, "email": user.email, "name": user.name}


@router.get("/session-data")
def session_data(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    count = db.scalar(
        select(RecommendationHistory.id)
        .where(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.id.desc())
        .limit(1)
    )
    return {"user_id": user.id, "recommendation_history_available": count is not None}


@router.get("/startup")
def startup_status():
    from ..config import get_settings
    settings = get_settings()
    return {
        "status": "ok",
        "gemini_configured": bool(settings.gemini_api_key) and not settings.mock_ai,
        "gemini_model": settings.gemini_model,
    }
```

## `app/services/__init__.py`

```python

```

## `app/services/gemini_service.py`

```python
import json
from typing import Any

from google import genai
from google.genai import types

from ..config import get_settings

settings = get_settings()


class GeminiService:
    def __init__(self):
        self.client = None
        if settings.gemini_api_key:
            self.client = genai.Client(api_key=settings.gemini_api_key)

    @property
    def available(self) -> bool:
        return bool(self.client) and not settings.mock_ai

    def generate(self, prompt: str, image_bytes: bytes | None = None, mime_type: str | None = None) -> dict[str, Any]:
        if not self.available:
            raise RuntimeError("Gemini is not configured")

        contents: list[Any] = [prompt]
        if image_bytes:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_bytes))
            contents.append(image)

        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.35,
                max_output_tokens=5000,
                response_mime_type="application/json",
            ),
        )

        text = response.text or ""
        return self._parse_json(text)

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
        return json.loads(cleaned)


gemini_service = GeminiService()
```

## `app/services/mock_catalog.py`

```python
from urllib.parse import quote_plus


HOME_CATALOG = [
    ("lighting", "LED ceiling light", "Amazon", 1899),
    ("lighting", "Minimal pendant light", "IKEA", 2499),
    ("furniture", "Compact 4-seat dining table", "IKEA", 12999),
    ("furniture", "Engineered wood side table", "Amazon", 2799),
    ("furniture", "Ergonomic study chair", "Amazon", 6499),
    ("decor", "Minimal wall art set", "Amazon", 1599),
    ("decor", "Neutral area rug", "IKEA", 4999),
    ("decor", "Indoor planter set", "IKEA", 2299),
    ("fans", "Energy-efficient ceiling fan", "Amazon", 3299),
    ("storage", "Modular storage unit", "IKEA", 7999),
]

PARTY_CATALOG = [
    ("catering", "Vegetarian buffet package", "Swiggy", 450),
    ("catering", "Party snack and dessert package", "Zomato", 350),
    ("venue", "Budget-friendly stay/venue option", "OYO", 3500),
    ("decoration", "Balloon and backdrop package", "Amazon", 2999),
    ("decoration", "Table decor starter set", "Amazon", 1899),
    ("entertainment", "Bluetooth party speaker", "Amazon", 4499),
]

JEWELRY_CATALOG = [
    ("earrings", "Minimal gold-tone drop earrings", "Amazon", 1499),
    ("necklace", "Pearl-inspired pendant necklace", "Amazon", 1999),
    ("bangles", "Classic bangle set", "Flipkart", 1799),
    ("earrings", "Crystal stud earrings", "Flipkart", 999),
    ("necklace", "Statement festive necklace", "Amazon", 2999),
]


def search_url(platform: str, name: str) -> str:
    query = quote_plus(name)
    if platform.lower() == "amazon":
        return f"https://www.amazon.in/s?k={query}"
    if platform.lower() == "flipkart":
        return f"https://www.flipkart.com/search?q={query}"
    if platform.lower() == "ikea":
        return f"https://www.ikea.com/in/en/search/?q={query}"
    if platform.lower() == "swiggy":
        return f"https://www.swiggy.com/search?query={query}"
    if platform.lower() == "zomato":
        return f"https://www.zomato.com/search?q={query}"
    if platform.lower() == "oyo":
        return f"https://www.oyorooms.com/search?location={query}"
    return f"https://www.google.com/search?q={query}"


def catalog_recommendations(planner: str, budget: float, limit: int = 8):
    catalog = {
        "home": HOME_CATALOG,
        "party": PARTY_CATALOG,
        "jewelry": JEWELRY_CATALOG,
    }[planner]
    # Keep fallback totals comfortably under the requested budget.
    target = budget * 0.85
    selected = []
    total = 0.0
    for category, name, platform, price in sorted(catalog, key=lambda x: x[3]):
        if total + price <= target or not selected:
            selected.append(
                {
                    "category": category,
                    "name": name,
                    "platform": platform,
                    "estimated_price": float(price),
                    "reason": "Budget-friendly catalog fallback option.",
                    "search_url": search_url(platform, name),
                }
            )
            total += price
        if len(selected) >= limit:
            break
    return selected
```

## `app/services/recommendation_service.py`

```python
import json
from typing import Any

from ..config import get_settings
from .gemini_service import gemini_service
from .mock_catalog import catalog_recommendations, search_url

settings = get_settings()


def _base_prompt(planner: str, payload: dict[str, Any]) -> str:
    return f"""
You are PocketSmart AI, a budget planning assistant.

Planner: {planner}
User input:
{json.dumps(payload, ensure_ascii=False, indent=2)}

Return ONLY valid JSON with exactly this shape:
{{
  "summary": "short practical summary",
  "allocations": {{"category": 0}},
  "recommendations": [
    {{
      "category": "category",
      "name": "suggested product/service",
      "platform": "Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO|Other",
      "estimated_price": 0,
      "reason": "why it fits"
    }}
  ]
}}

Rules:
- Respect the total budget and do not recommend an impossible total.
- Estimated prices are estimates, not verified live prices.
- Never claim that you checked live inventory or a real-time price.
- Keep recommendations practical and concise.
- Use Indian Rupees for all numeric prices.
- Prefer the platforms relevant to the planner.
"""


def _fallback(planner: str, budget: float, payload: dict[str, Any], reason: str) -> dict[str, Any]:
    items = catalog_recommendations(planner, budget)
    total = sum(item["estimated_price"] for item in items)
    return {
        "summary": f"Fallback recommendations were generated because {reason}.",
        "allocations": _fallback_allocations(planner, budget),
        "recommendations": items,
        "total_estimated": round(total, 2),
        "budget_remaining": round(max(0, budget - total), 2),
        "source_mode": "mock-catalog",
        "model": None,
    }


def _fallback_allocations(planner: str, budget: float):
    if planner == "home":
        ratios = {"furniture": .45, "lighting": .15, "decor": .20, "storage": .20}
    elif planner == "party":
        ratios = {"catering": .45, "venue": .25, "decoration": .15, "entertainment": .15}
    else:
        ratios = {"necklace": .45, "earrings": .30, "bangles": .25}
    return {k: round(budget * v, 2) for k, v in ratios.items()}


def recommend(planner: str, budget: float, payload: dict[str, Any], image_bytes=None, mime_type=None):
    if settings.mock_ai or not gemini_service.available:
        return _fallback(planner, budget, payload, "Gemini is disabled or no API key is configured")

    try:
        data = gemini_service.generate(
            _base_prompt(planner, payload),
            image_bytes=image_bytes,
            mime_type=mime_type,
        )
        raw_items = data.get("recommendations", [])
        items = []
        total = 0.0

        for raw in raw_items[:12]:
            try:
                price = max(0.0, float(raw.get("estimated_price", 0)))
            except (TypeError, ValueError):
                continue
            platform = str(raw.get("platform", "Other"))
            name = str(raw.get("name", "Recommendation"))[:200]
            item = {
                "category": str(raw.get("category", "general"))[:80],
                "name": name,
                "platform": platform[:50],
                "estimated_price": price,
                "reason": str(raw.get("reason", ""))[:500],
                "search_url": search_url(platform, name),
            }
            if total + price <= budget:
                items.append(item)
                total += price

        if not items:
            return _fallback(planner, budget, payload, "the AI response did not contain usable recommendations")

        return {
            "summary": str(data.get("summary", "AI-generated budget recommendations.")),
            "allocations": data.get("allocations", _fallback_allocations(planner, budget)),
            "recommendations": items,
            "total_estimated": round(total, 2),
            "budget_remaining": round(max(0, budget - total), 2),
            "source_mode": "gemini",
            "model": settings.gemini_model,
        }
    except Exception:
        return _fallback(planner, budget, payload, "the AI service was unavailable or returned invalid data")
```

## `app/static/css/styles.css`

```css
:root{
  --bg:#f6f7fb;--surface:#fff;--text:#171923;--muted:#69707d;
  --accent:#635bff;--accent2:#eeeaff;--border:#e4e6ed;--shadow:0 12px 36px rgba(22,25,40,.08)
}
*{box-sizing:border-box}body{margin:0;font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:var(--bg);color:var(--text)}
a{color:inherit;text-decoration:none}.nav{height:72px;background:#fff;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 max(24px,calc((100vw - 1180px)/2));position:sticky;top:0;z-index:10}.brand{font-size:21px;font-weight:800}.brand span{color:var(--accent)}nav{display:flex;align-items:center;gap:20px;font-size:14px}.nav-cta{background:var(--text);color:#fff;padding:10px 15px;border-radius:10px}.link-button{background:none;border:0;font:inherit;cursor:pointer;color:var(--text)}
.container{max-width:1180px;margin:auto;padding:54px 24px 80px}.hero{display:grid;grid-template-columns:1.5fr 1fr;gap:50px;align-items:center;min-height:520px}.eyebrow{font-size:12px;letter-spacing:.14em;font-weight:800;color:var(--accent);margin:0 0 12px}.hero h1{font-size:clamp(42px,6vw,72px);line-height:1.02;letter-spacing:-.05em;margin:0 0 22px}.lead{font-size:19px;line-height:1.7;color:var(--muted);max-width:650px}.hero-actions{display:flex;gap:12px;margin-top:28px}.button{display:inline-flex;justify-content:center;align-items:center;background:var(--accent);color:white;border:0;border-radius:11px;padding:13px 18px;font-weight:750;cursor:pointer;font-size:15px}.button.secondary{background:var(--accent2);color:var(--accent)}.hero-card{background:#11131c;color:#fff;border-radius:28px;padding:36px;box-shadow:var(--shadow)}.mini-label{font-size:11px;letter-spacing:.14em;opacity:.65}.budget-number{font-size:30px;font-weight:800;margin:55px 0 20px}.progress{height:12px;background:#30333f;border-radius:99px;overflow:hidden}.progress span{display:block;width:72%;height:100%;background:#fff;border-radius:99px}.muted{color:var(--muted);line-height:1.6}.hero-card .muted{color:#b6bac5}
.section{margin-top:65px}.section-heading{margin-bottom:22px}.section-heading h2,.page-heading h1{margin:0;letter-spacing:-.03em}.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.feature-card{background:var(--surface);border:1px solid var(--border);border-radius:18px;padding:25px;transition:.2s}.feature-card:hover{transform:translateY(-2px);box-shadow:var(--shadow)}.feature-card span{font-size:30px}.feature-card h3{margin:18px 0 8px}.feature-card p{color:var(--muted);line-height:1.6}.notice{margin-top:45px;padding:17px 19px;background:#fff7e5;border:1px solid #f3dfb0;border-radius:12px;color:#745719}
.footer{border-top:1px solid var(--border);padding:26px max(24px,calc((100vw - 1180px)/2));display:flex;justify-content:space-between;color:var(--muted);font-size:13px;background:#fff}.auth-card,.planner-shell{max-width:620px;margin:35px auto;background:#fff;border:1px solid var(--border);border-radius:22px;padding:35px;box-shadow:var(--shadow)}.auth-card h1,.planner-shell h1{font-size:38px;letter-spacing:-.04em}.form,.planner-form{display:grid;gap:18px;margin:28px 0}.form label,.planner-form label{display:grid;gap:8px;font-size:14px;font-weight:700}input,select,textarea{font:inherit;border:1px solid var(--border);border-radius:10px;padding:12px 13px;background:#fff;color:var(--text)}select[multiple]{min-height:130px}textarea{min-height:100px;resize:vertical}.form-message{min-height:20px;font-size:14px}.form-message.error{color:#b42318}.form-message.success{color:#067647}.loading{margin-top:18px;padding:14px;background:var(--accent2);border-radius:10px;color:var(--accent);font-weight:700}.hidden{display:none}.page-heading{margin-bottom:30px}.page-heading h1{font-size:48px}.row-between{display:flex;justify-content:space-between;align-items:center}.history-list{display:grid;gap:10px}.history-row{display:flex;align-items:center;justify-content:space-between;background:#fff;border:1px solid var(--border);border-radius:13px;padding:18px 20px}.history-row div{display:grid;gap:5px}.history-row span{color:var(--muted);font-size:13px}.empty{padding:35px;text-align:center;background:#fff;border:1px dashed var(--border);border-radius:15px;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.stats>div{background:#fff;border:1px solid var(--border);border-radius:14px;padding:18px}.stats span{display:block;color:var(--muted);font-size:12px;margin-bottom:7px}.stats strong{font-size:21px}.recommendation-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.recommendation-card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:20px}.card-top{display:flex;gap:6px;justify-content:space-between}.pill{font-size:11px;background:var(--accent2);color:var(--accent);padding:5px 8px;border-radius:99px}.recommendation-card h3{margin:20px 0 9px}.price{font-size:24px;font-weight:800}.recommendation-card p{color:var(--muted);line-height:1.5;min-height:60px}.recommendation-card a{color:var(--accent);font-weight:700;font-size:14px}.allocation-list{max-width:650px;background:#fff;border:1px solid var(--border);border-radius:14px;overflow:hidden}.allocation-list div{display:flex;justify-content:space-between;padding:15px 18px;border-bottom:1px solid var(--border)}.allocation-list div:last-child{border:0}
@media(max-width:800px){.hero{grid-template-columns:1fr}.grid-3,.recommendation-grid,.stats{grid-template-columns:1fr}.footer{display:block}.footer div+div{margin-top:8px}nav{gap:10px}.nav{padding:0 16px}.container{padding:35px 16px 60px}}
```

## `app/static/js/app.js`

```javascript
async function api(url, options = {}) {
  const opts = {...options, credentials: "same-origin"};
  if (opts.body && typeof opts.body !== "string" && !(opts.body instanceof FormData)) {
    opts.headers = {...opts.headers, "Content-Type": "application/json"};
    opts.body = JSON.stringify(opts.body);
  }
  const response = await fetch(url, opts);
  let data = {};
  try { data = await response.json(); } catch {}
  return {ok: response.ok, status: response.status, data};
}

function showMessage(message, error=false) {
  const el = document.getElementById("form-message");
  if (!el) return;
  el.textContent = message;
  el.className = "form-message " + (error ? "error" : "success");
}

function setLoading(active) {
  const el = document.getElementById("loading");
  if (el) el.classList.toggle("hidden", !active);
}

async function logout() {
  await api("/api/auth/logout", {method:"POST"});
  location.href="/";
}
```

## `app/templates/base.html`

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{% block title %}PocketSmart AI{% endblock %}</title>
  <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
<header class="nav">
  <a class="brand" href="/">PocketSmart <span>AI</span></a>
  <nav>
    <a href="/">Home</a>
    {% if user %}
      <a href="/dashboard">Dashboard</a>
      <a href="/history">History</a>
      <button class="link-button" onclick="logout()">Logout</button>
    {% else %}
      <a href="/login">Login</a>
      <a class="nav-cta" href="/register">Get started</a>
    {% endif %}
  </nav>
</header>

<main class="container">
  {% block content %}{% endblock %}
</main>

<footer class="footer">
  <div>© 2026 PocketSmart AI</div>
  <div>Budget first. Recommendations second.</div>
</footer>
<script src="/static/js/app.js"></script>
{% block scripts %}{% endblock %}
</body>
</html>
```

## `app/templates/dashboard.html`

```html
{% extends "base.html" %}
{% block title %}Dashboard — PocketSmart AI{% endblock %}
{% block content %}
<div class="page-heading">
  <p class="eyebrow">DASHBOARD</p>
  <h1>Hello, {{ user.name }}.</h1>
  <p class="muted">Choose a planner or reopen a recent recommendation.</p>
</div>

<div class="grid-3">
  <a class="feature-card" href="/planner/home"><span>🏠</span><h3>Home</h3><p>Furniture, lighting and decor.</p></a>
  <a class="feature-card" href="/planner/party"><span>🎉</span><h3>Party</h3><p>Food, venue and decoration.</p></a>
  <a class="feature-card" href="/planner/jewelry"><span>💎</span><h3>Jewelry</h3><p>Occasion and outfit matching.</p></a>
</div>

<section class="section">
  <div class="section-heading row-between"><h2>Recent plans</h2><a href="/history">View all</a></div>
  {% if recent %}
  <div class="history-list">
    {% for item in recent %}
    <a class="history-row" href="/recommendations/{{ item.id }}">
      <div><strong>{{ item.planner|title }}</strong><span>{{ item.created_at.strftime("%d %b %Y, %I:%M %p") }}</span></div>
      <strong>₹{{ "{:,.0f}".format(item.budget) }}</strong>
    </a>
    {% endfor %}
  </div>
  {% else %}
  <div class="empty">No recommendations yet. Start with a planner above.</div>
  {% endif %}
</section>
{% endblock %}
```

## `app/templates/history.html`

```html
{% extends "base.html" %}
{% block title %}History — PocketSmart AI{% endblock %}
{% block content %}
<div class="page-heading">
  <p class="eyebrow">HISTORY</p>
  <h1>Your recommendation history</h1>
</div>
{% if rows %}
<div class="history-list">
{% for item in rows %}
<a class="history-row" href="/recommendations/{{ item.id }}">
  <div><strong>{{ item.planner|title }} planner</strong><span>{{ item.created_at.strftime("%d %b %Y, %I:%M %p") }}</span></div>
  <strong>₹{{ "{:,.0f}".format(item.budget) }}</strong>
</a>
{% endfor %}
</div>
{% else %}
<div class="empty">Nothing saved yet.</div>
{% endif %}
{% endblock %}
```

## `app/templates/index.html`

```html
{% extends "base.html" %}
{% block title %}PocketSmart AI — Smart Budget Assistant{% endblock %}
{% block content %}
<section class="hero">
  <div>
    <p class="eyebrow">GENAI BUDGET ASSISTANT</p>
    <h1>Plan smarter without losing control of your budget.</h1>
    <p class="lead">PocketSmart AI turns a budget and a few preferences into practical recommendations for homes, parties, and jewelry.</p>
    <div class="hero-actions">
      {% if user %}
      <a class="button" href="/dashboard">Open dashboard</a>
      {% else %}
      <a class="button" href="/register">Create free account</a>
      <a class="button secondary" href="/login">Login</a>
      {% endif %}
    </div>
  </div>
  <div class="hero-card">
    <div class="mini-label">SMART PLANNERS</div>
    <div class="budget-number">₹ Your budget</div>
    <div class="progress"><span></span></div>
    <div class="muted">AI suggestions stay inside your stated budget.</div>
  </div>
</section>

<section class="section">
  <div class="section-heading">
    <p class="eyebrow">THREE WORKFLOWS</p>
    <h2>One assistant, multiple life needs.</h2>
  </div>
  <div class="grid-3">
    <a class="feature-card" href="/planner/home"><span>🏠</span><h3>Home Interior</h3><p>Allocate a decor budget across furniture, lighting, storage, and style.</p></a>
    <a class="feature-card" href="/planner/party"><span>🎉</span><h3>Party Planner</h3><p>Balance food, venue, decoration, and entertainment for your guest count.</p></a>
    <a class="feature-card" href="/planner/jewelry"><span>💎</span><h3>Jewelry</h3><p>Match jewelry to your occasion and style, with optional outfit-image analysis.</p></a>
  </div>
</section>

<section class="notice">
  <strong>Data note:</strong> product prices shown by the demo catalog are estimates. The app does not claim live marketplace inventory.
</section>
{% endblock %}
```

## `app/templates/login.html`

```html
{% extends "base.html" %}
{% block title %}Login — PocketSmart AI{% endblock %}
{% block content %}
<div class="auth-card">
  <p class="eyebrow">WELCOME BACK</p>
  <h1>Login</h1>
  <p class="muted">Access your saved recommendation history.</p>
  <form id="login-form" class="form">
    <label>Email<input name="email" type="email" required></label>
    <label>Password<input name="password" type="password" minlength="8" required></label>
    <button class="button" type="submit">Login</button>
    <div id="form-message" class="form-message"></div>
  </form>
  <p class="muted">New here? <a href="/register">Create an account</a>.</p>
</div>
{% endblock %}
{% block scripts %}
<script>
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const result = await api("/api/auth/login", {method:"POST", body:JSON.stringify(data)});
  if (result.ok) location.href="/dashboard";
  else showMessage(result.data.detail || "Login failed", true);
});
</script>
{% endblock %}
```

## `app/templates/planner.html`

```html
{% extends "base.html" %}
{% set titles = {"home":"Home Interior Budget Planner","party":"Party Budget Planner","jewelry":"Jewelry Budget Planner"} %}
{% block title %}{{ titles[planner] }} — PocketSmart AI{% endblock %}
{% block content %}
<div class="planner-shell">
  <div class="page-heading">
    <p class="eyebrow">AI PLANNER</p>
    <h1>{{ titles[planner] }}</h1>
    <p class="muted">Set a hard budget. PocketSmart AI will prioritize useful options within it.</p>
  </div>

  {% if planner == "home" %}
  <form id="planner-form" class="planner-form">
    <input type="hidden" name="planner" value="home">
    <label>Total budget (₹)<input name="budget" type="number" min="1" step="100" required></label>
    <label>Rooms
      <select name="rooms" multiple required>
        <option selected>Living Room</option><option>Bedroom</option><option>Kitchen</option><option>Dining Room</option>
      </select>
    </label>
    <label>Style<select name="style"><option>Modern</option><option>Minimal</option><option>Traditional</option><option>Scandinavian</option></select></label>
    <label>Notes<textarea name="notes" placeholder="Colors, must-have items, constraints..."></textarea></label>
    <label>Quantities (optional JSON)<input name="items" value='{"lights":2,"fans":1}'></label>
    <button class="button" type="submit">Generate home plan</button>
  </form>

  {% elif planner == "party" %}
  <form id="planner-form" class="planner-form">
    <input type="hidden" name="planner" value="party">
    <label>Total budget (₹)<input name="budget" type="number" min="1" step="100" required></label>
    <label>Guest count<input name="guests" type="number" min="1" required></label>
    <label>Event type<select name="event_type"><option>Birthday</option><option>Corporate</option><option>Wedding</option><option>Family gathering</option></select></label>
    <label>Venue preference<input name="venue" placeholder="Home, hall, restaurant, flexible"></label>
    <label>Notes<textarea name="notes" placeholder="Food preferences, theme, location notes..."></textarea></label>
    <button class="button" type="submit">Generate party plan</button>
  </form>

  {% else %}
  <form id="planner-form" class="planner-form" enctype="multipart/form-data">
    <input type="hidden" name="planner" value="jewelry">
    <label>Budget (₹)<input name="budget" type="number" min="1" step="100" required></label>
    <label>Occasion<input name="occasion" placeholder="Wedding, party, office event..." required></label>
    <label>Style<select name="style"><option>Elegant</option><option>Minimal</option><option>Traditional</option><option>Statement</option><option>Contemporary</option></select></label>
    <label>Metal preference<select name="metal"><option>Any</option><option>Gold tone</option><option>Silver tone</option><option>Rose gold tone</option></select></label>
    <label>Outfit image (optional)<input name="outfit_image" type="file" accept="image/jpeg,image/png,image/webp"></label>
    <label>Notes<textarea name="notes" placeholder="Colors, neckline, preferred jewelry type..."></textarea></label>
    <button class="button" type="submit">Generate jewelry plan</button>
  </form>
  {% endif %}
  <div id="loading" class="loading hidden">Generating your plan…</div>
  <div id="form-message" class="form-message"></div>
</div>
{% endblock %}
{% block scripts %}
<script>
const planner = "{{ planner }}";
document.getElementById("planner-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  setLoading(true);
  let options = {method:"POST"};
  if (planner === "jewelry") {
    options.body = new FormData(form);
  } else {
    const fd = new FormData(form);
    const data = Object.fromEntries(fd);
    if (planner === "home") {
      data.budget = Number(data.budget);
      data.rooms = fd.getAll("rooms");
      try { data.items = JSON.parse(data.items || "{}"); } catch { data.items = {}; }
    } else {
      data.budget = Number(data.budget);
      data.guests = Number(data.guests);
    }
    delete data.planner;
    options.headers = {"Content-Type":"application/json"};
    options.body = JSON.stringify(data);
  }
  const result = await api("/api/generate-" + planner, options);
  setLoading(false);
  if (result.ok) {
    localStorage.setItem("latestRecommendation", JSON.stringify(result.data));
    location.href = "/dashboard";
  } else {
    showMessage(result.data.detail || "Could not generate recommendations", true);
  }
});
</script>
{% endblock %}
```

## `app/templates/recommendations.html`

```html
{% extends "base.html" %}
{% block title %}Recommendation — PocketSmart AI{% endblock %}
{% block content %}
<div class="page-heading">
  <p class="eyebrow">{{ history.planner|upper }} RECOMMENDATION</p>
  <h1>Your plan</h1>
  <p class="muted">{{ result.summary }}</p>
</div>

<div class="stats">
  <div><span>Budget</span><strong>₹{{ "{:,.0f}".format(result.budget) }}</strong></div>
  <div><span>Estimated total</span><strong>₹{{ "{:,.0f}".format(result.total_estimated) }}</strong></div>
  <div><span>Remaining</span><strong>₹{{ "{:,.0f}".format(result.budget_remaining) }}</strong></div>
  <div><span>Source</span><strong>{{ result.source_mode|title }}</strong></div>
</div>

<section class="section">
  <div class="section-heading"><h2>Recommendations</h2></div>
  <div class="recommendation-grid">
  {% for item in result.recommendations %}
    <article class="recommendation-card">
      <div class="card-top"><span class="pill">{{ item.category }}</span><span class="pill">{{ item.platform }}</span></div>
      <h3>{{ item.name }}</h3>
      <div class="price">₹{{ "{:,.0f}".format(item.estimated_price) }}</div>
      <p>{{ item.reason }}</p>
      {% if item.search_url %}<a href="{{ item.search_url }}" target="_blank" rel="noopener noreferrer">Search platform ↗</a>{% endif %}
    </article>
  {% endfor %}
  </div>
</section>

<section class="section">
<h2>Budget allocation</h2>
<div class="allocation-list">
{% for key, value in result.allocations.items() %}
<div><span>{{ key|replace("_"," ")|title }}</span><strong>₹{{ "{:,.0f}".format(value) }}</strong></div>
{% endfor %}
</div>
</section>
{% endblock %}
```

## `app/templates/register.html`

```html
{% extends "base.html" %}
{% block title %}Register — PocketSmart AI{% endblock %}
{% block content %}
<div class="auth-card">
  <p class="eyebrow">GET STARTED</p>
  <h1>Create your account</h1>
  <p class="muted">Save plans and revisit your recommendations.</p>
  <form id="register-form" class="form">
    <label>Name<input name="name" required minlength="2"></label>
    <label>Email<input name="email" type="email" required></label>
    <label>Password<input name="password" type="password" minlength="8" required></label>
    <button class="button" type="submit">Create account</button>
    <div id="form-message" class="form-message"></div>
  </form>
  <p class="muted">Already registered? <a href="/login">Login</a>.</p>
</div>
{% endblock %}
{% block scripts %}
<script>
document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  const result = await api("/api/auth/register", {method:"POST", body:JSON.stringify(data)});
  if (result.ok) location.href="/dashboard";
  else showMessage(result.data.detail || "Registration failed", true);
});
</script>
{% endblock %}
```

## `data/.gitkeep`

```text

```

## `docker-compose.yml`

```yaml
services:
  pocketsmart:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - pocketsmart_data:/app/data

volumes:
  pocketsmart_data:
```

## `requirements.txt`

```text
fastapi>=0.115,<1
uvicorn[standard]>=0.30,<1
jinja2>=3.1,<4
python-multipart>=0.0.9,<1
pydantic-settings>=2.5,<3
sqlalchemy>=2.0,<3
PyJWT>=2.9,<3
werkzeug>=3.1,<4
google-genai>=1.30,<2
Pillow>=10,<12
httpx>=0.27,<1
pytest>=8,<9

email-validator>=2.2,<3
```

## `run.py`

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
```

## `tests/conftest.py`

```python
import os
os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["MOCK_AI"] = "true"
os.environ["SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
```

## `tests/test_api.py`

```python
def register(client):
    response = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "strong-password",
    })
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_and_session(client):
    token = register(client)
    response = client.get("/api/session-info", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["authenticated"] is True


def test_home_party_history(client):
    token = register(client)
    headers = {"Authorization": f"Bearer {token}"}

    home = client.post("/api/generate-home", headers=headers, json={
        "budget": 30000,
        "rooms": ["Living Room", "Bedroom"],
        "style": "Modern",
        "notes": "Warm neutrals",
        "items": {"lights": 2, "fans": 1},
    })
    assert home.status_code == 200
    assert home.json()["planner"] == "home"
    assert home.json()["total_estimated"] <= 30000

    party = client.post("/api/generate-party", headers=headers, json={
        "budget": 25000,
        "guests": 30,
        "event_type": "Birthday",
        "venue": "Home",
        "notes": "",
    })
    assert party.status_code == 200

    history = client.get("/api/history", headers=headers)
    assert history.status_code == 200
    assert len(history.json()) == 2


def test_jewelry_multipart(client):
    token = register(client)
    response = client.post(
        "/api/generate-jewelry",
        headers={"Authorization": f"Bearer {token}"},
        data={
            "budget": "10000",
            "occasion": "Wedding",
            "style": "Elegant",
            "metal": "Gold tone",
            "notes": "Simple necklace",
        },
    )
    assert response.status_code == 200
    assert response.json()["planner"] == "jewelry"


def test_unauthenticated_api_rejected(client):
    response = client.get("/api/history")
    assert response.status_code == 401
```

