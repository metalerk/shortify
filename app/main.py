from fastapi import FastAPI
from app.api.urls import router
from app.data.database import initialize_database
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()

# initialize db
initialize_database()

# metrics
Instrumentator().instrument(app).expose(app)

# API routes
app.include_router(router)
