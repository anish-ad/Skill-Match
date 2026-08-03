from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health

app = FastAPI(title="SkillMatch API")

# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the health check router under /api
app.include_router(health.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to SkillMatch API"}