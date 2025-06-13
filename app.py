from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db
from core.middleware import setup_middleware

app = FastAPI(
    title="IslamicQA",
    description="Islamic Question and Answer API",
    version="1.0.0"
)

# Setup middleware
setup_middleware(app)

@app.on_event("startup")
async def on_startup():
    await init_db()

# Import and include routers
from api.v1.router import api_router
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)