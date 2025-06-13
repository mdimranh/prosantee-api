from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import JWTTokenMiddleware

def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware for the application.
    
    Args:
        app: FastAPI application instance
    """
    # CORS middleware configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Authentication middleware
    app.add_middleware(JWTTokenMiddleware)
    
    # Add more middleware here as needed