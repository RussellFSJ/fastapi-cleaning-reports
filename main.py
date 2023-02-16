import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from routes import index, cleaningReports

load_dotenv()

app = FastAPI(default_response_class=ORJSONResponse)

origins = ["http://localhost:8090"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(os.environ["DATABASE_URL"])
    app.mongodb = app.mongodb_client[os.environ["DATABASE_NAME"]]


@app.on_event("shutdown")
async def startup_db_client():
    app.mongodb_client.close()


app.include_router(index.router, prefix="")
app.include_router(cleaningReports.router, prefix="/cleaning_reports")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=int(os.environ["PORT"]),
        reload=bool(os.environ["DEBUG_MODE"]),
    )
