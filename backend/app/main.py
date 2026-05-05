import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.config import settings
from app.database import create_tables, close_connections
from app.api import users, experiments, uploads, analysis, visualization

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up M. abscessus Tolerance Platform API")
    await create_tables()
    yield
    await close_connections()
    logger.info("Shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "REST API for M. abscessus antibiotic tolerance research platform. "
        "Integrates high-content imaging, CRISPRi, and Tn-seq data."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
prefix = settings.API_V1_PREFIX
app.include_router(users.router, prefix=f"{prefix}/auth", tags=["Authentication"])
app.include_router(users.users_router, prefix=f"{prefix}/users", tags=["Users"])
app.include_router(
    experiments.router, prefix=f"{prefix}/experiments", tags=["Experiments"]
)
app.include_router(uploads.router, prefix=f"{prefix}/upload", tags=["File Upload"])
app.include_router(analysis.router, prefix=f"{prefix}/analysis", tags=["Analysis"])
app.include_router(
    visualization.router,
    prefix=f"{prefix}/visualization",
    tags=["Visualization"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "M. abscessus Tolerance Platform API",
        "docs": "/docs",
        "version": settings.APP_VERSION,
    }
