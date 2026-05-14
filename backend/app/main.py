from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import verify_routes, health_routes

app = FastAPI(
    title="TruthLens API",
    description="AI Hallucination Detection & Verification System",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_routes.router, prefix="/api", tags=["Health"])
app.include_router(verify_routes.router, prefix="/api", tags=["Verification"])

@app.get("/")
async def root():
    return {"message": "Welcome to TruthLens API"}
