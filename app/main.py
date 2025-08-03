from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.status import status_router
from app.api.v1.endpoints import feedback, scenario, submission, upload
from app.core.database import init_db
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    # Initialize the database
    await init_db()
    yield

is_production = settings.ENV == "production"

app = FastAPI(
    lifespan=lifespan,
    title="Monolog Core",
    description="Backend API for Monolog learning platform - AI-powered communication training",
    version="1.0.0",
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://usemonolog.com", "https://www.usemonolog.com", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(feedback.router, prefix="/api/v1/feedback", tags=["feedback"])
app.include_router(scenario.router, prefix="/api/v1/scenario", tags=["scenario"])
app.include_router(submission.router, prefix="/api/v1/submission", tags=["submission"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["upload"]) 

# Include status endpoints
app.include_router(status_router, prefix="/api/v1/status", tags=["status"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Monolog Core API",
        "description": "AI-powered communication training platform",
        "docs": "/docs",
        "version": "1.0.0"
    }