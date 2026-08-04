from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, auth, dashboard

app = FastAPI(title="SkillMatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])

@app.get("/")
async def root():
    return {"message": "Welcome to SkillMatch API"}