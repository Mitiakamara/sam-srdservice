import os
from fastapi import FastAPI
from dotenv import load_dotenv

from srd_service import get_router, init_srd_service, get_health_router

load_dotenv()

app = FastAPI(title="S.A.M. – SRDService", version="1.0")

# Initialize SRD loader at startup
@app.on_event("startup")
async def startup_event():
    base_path = os.getenv("SRD_BASE_PATH", "./srd")
    init_srd_service(base_path)

# Routers
app.include_router(get_router(), prefix="/srd", tags=["SRD"])
app.include_router(get_health_router(), tags=["Health"])