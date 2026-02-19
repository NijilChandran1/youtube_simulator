from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import video_analysis, events, sessions, video_list

app = FastAPI(
    title="EPG Training Feedback Loop API",
    description="API for EPG training video analysis and feedback",
    version="0.1.0",
    debug=settings.DEBUG
)

app.include_router(video_analysis.router)
app.include_router(events.router)
app.include_router(sessions.router)
app.include_router(video_list.router)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "EPG Training API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
