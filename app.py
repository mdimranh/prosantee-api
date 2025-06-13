from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db

app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application with SQLModel and best practices",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

# Import and include routers
from api.v1.router import api_router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)