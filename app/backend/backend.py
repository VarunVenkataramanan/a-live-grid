from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.backend.core.config import settings
from app.backend.routers import posts

app = FastAPI(
	title=settings.PROJECT_NAME,
	version="1.0.0",
	description="A-Live-Grid Social Media Platform API",
)

# CORS middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # In production, specify your frontend domain
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Include routers
app.include_router(posts.router, prefix=f"{settings.API_V1_STR}/posts", tags=["posts"])


@app.get("/")
async def root():
	return {
		"message": "Welcome to A-Live-Grid API",
		"version": "1.0.0",
		"docs": "/docs",
		"redoc": "/redoc",
	}


@app.get("/health")
async def health_check():
	return {"status": "healthy", "service": "a-live-grid-api"}
