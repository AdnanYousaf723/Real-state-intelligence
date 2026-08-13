from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reli.api.routes import health, properties, leads, signals, pipeline

app = FastAPI(
    title="RELI - Real Estate Lead Intelligence",
    version="1.0.0",
    description="Automated real-estate data pipeline API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(properties.router, prefix="/api/v1", tags=["Properties"])
app.include_router(leads.router, prefix="/api/v1", tags=["Leads"])
app.include_router(signals.router, prefix="/api/v1", tags=["Signals"])
app.include_router(pipeline.router, prefix="/api/v1", tags=["Pipeline"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("reli.api.main:app", host="0.0.0.0", port=8000, reload=True)
