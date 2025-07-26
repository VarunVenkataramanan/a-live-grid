from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import posts
from app.core.config import settings

app = FastAPI(
    title="A-Live-Grid API",
    description="Proactive Urban Intelligence Platform Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(posts.router, prefix="/api/v1/posts", tags=["Posts"])

@app.get("/")
async def root():
    return {"message": "Welcome to A-Live-Grid API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 