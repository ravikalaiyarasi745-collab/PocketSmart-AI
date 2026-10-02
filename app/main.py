from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import Base,engine
from . import models  
from .routes.auth import router as auth_router
from .routes.pages import router as pages_router
from .routes.recommendations import router as recommendation_router
from .routes.dashboard import router as dashboard_router
from .routes.expenses import router as expenses_router
from .routes.income import router as income_router
from .routes.budget import router as budget_router
from .routes.assistant import router as assistant_router
from .routes.interior import router as interior_router
from .routes.party import router as party_router
from .routes.jewelry import router as jewelry_router

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
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(recommendation_router)
app.include_router(dashboard_router)
app.include_router(expenses_router)
app.include_router(income_router)
app.include_router(budget_router)
app.include_router(assistant_router)
app.include_router(interior_router)
app.include_router(party_router)
app.include_router(jewelry_router)


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name}



